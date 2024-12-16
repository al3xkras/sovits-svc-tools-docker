import os
import subprocess
from pyannote.audio import Pipeline
from pydub import AudioSegment
import typer
import mimetypes
import json
import torch
import logging
import gc
import torch
from pydub.utils import mediainfo
import re

device = torch.device("cuda")
HOME = os.environ["HOME"]

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AudioProcessor:
    UVR5_PATH = os.path.join(HOME, 'uvr5')
    DEFAULT_INPUT_DIR = os.path.join(HOME, 'share/inputs')
    DEFAULT_OUTPUT_DIR = os.path.join(HOME, 'share/outputs')
    DEFAULT_MODEL = os.path.join(UVR5_PATH, 'models/Demucs_Models/v3_v4_repo/hdemucs_mmi.yaml')

    def __init__(self, input_dir, output_dir, uvr5_model):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.uvr5_model = uvr5_model
        os.makedirs(self.output_dir, exist_ok=True)
        self.pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1").to(device)
        logging.info("Initialized AudioProcessor with input directory: %s and output directory: %s", self.input_dir, self.output_dir)

    def extract_audio_from_videos(self):
        logging.info("Extracting audio from video files in %s", self.input_dir)
        for file_name in os.listdir(self.input_dir):
            file_path = os.path.join(self.input_dir, file_name)
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type and mime_type.startswith('video'):
                audio_output_path = os.path.splitext(file_path)[0] + '.wav'
                logging.info("Extracting audio from %s to %s", file_path, audio_output_path)
                subprocess.run([
                    'ffmpeg', '-i', file_path, '-ac', '1', '-ar', '22050', audio_output_path
                ], check=True)
                os.remove(file_path)
                gc.collect()
                logging.info("Deleted original video file %s", file_path)
    
    def split_audio_into_chunks(self, input_file):
        logging.info("Checking duration of audio file %s", input_file)
        info = mediainfo(input_file)
        duration = float(info['duration'])
        chunk_duration = 300
        
        if duration > chunk_duration+1:
            logging.info("Splitting audio file %s into chunks", input_file)
            file_base = os.path.splitext(input_file)[0]
            subprocess.run([
                'ffmpeg', '-i', input_file, '-f', 'segment', '-segment_time', str(chunk_duration),
                '-c', 'copy', f'{file_base}_%03d.wav'
            ], check=True)
            os.remove(input_file)
            logging.info("Deleted original audio file %s after splitting", input_file)
        
    def delete_too_short_audios(self, audio_files):
        min_duration = 1
        for input_file in audio_files:
            info = mediainfo(input_file)
            duration = float(info.get('duration', 0))
            if duration > min_duration:
                continue
            logging.info("Deleted audio file %s because it is too short", input_file)
            os.remove(input_file)
    
    def combine_audio_chunks(self, base_name):
        chunk_files = sorted([
            f for f in os.listdir(self.output_dir)
            if f.startswith(base_name) and not "combined" in f and
            mimetypes.guess_type(f)[0] and 'audio' in mimetypes.guess_type(f)[0]
        ])

        if not chunk_files:
            logging.info("No chunks found for %s", base_name)
            return None

        with open(os.path.join(self.output_dir, f'{base_name}_chunks.txt'), 'w') as f:
            for chunk in chunk_files:
                f.write(f"file '{os.path.join(self.output_dir, chunk)}'\n")

        combined_output = os.path.join(self.output_dir, f'{base_name}_combined.wav')
        
        subprocess.run([
            'ffmpeg', '-f', 'concat', '-safe', '0', '-i',
            os.path.join(self.output_dir, f'{base_name}_chunks.txt'),
            '-c', 'copy', combined_output, '-n'
        ], check=True)
        
        for chunk in chunk_files:
            os.remove(os.path.join(self.output_dir, chunk))
        os.remove(os.path.join(self.output_dir, f'{base_name}_chunks.txt'))

        return combined_output
            
    def extract_vocals(self, input_files, output_dir):
        logging.info("Extracting vocals from audio files")
        if isinstance(input_files, str):
            input_files = [input_files]
        
        subprocess.run([
            'audio-separator', *input_files,
            '--single_stem', 'Vocals',
            '--output_dir', output_dir,
            '--model_file_dir', os.path.dirname(self.uvr5_model),
            '-m', os.path.basename(self.uvr5_model),
            '--output_format', 'WAV',
            '--sample_rate', '44100'
        ], check=True)
        
        logging.info("Vocal extraction complete. Output saved to %s", output_dir)
        
        gc.collect()
        torch.cuda.empty_cache()
        

    def diarize_audio(self, input_file, output_path):
        logging.info("Diarizing audio file %s", input_file)
        with torch.no_grad():
            diarization = self.pipeline(input_file)
        audio = AudioSegment.from_wav(input_file)

        for i, segment in enumerate(diarization.itertracks(yield_label=True)):
            start_time, end_time, speaker_id = segment[0].start, segment[0].end, segment[2]
            start_ms, end_ms = int(start_time * 1000), int(end_time * 1000)
            
            # do not save samples shorter than 1 second.
            if end_ms - start_ms < 1000: 
                continue
            
            speaker_audio = audio[start_ms:end_ms]
            
            speaker_dir = os.path.join(output_path, speaker_id.lower())
            os.makedirs(speaker_dir, exist_ok=True)

            output_file = os.path.join(speaker_dir, f'sample_{i}.wav')
            speaker_audio.export(output_file, format="wav")
        
        gc.collect()
        torch.cuda.empty_cache()


    def get_music_files(self):
        return [
            os.path.join(self.input_dir, file_name)
            for file_name in os.listdir(self.input_dir)
            if mimetypes.guess_type(file_name)[0] and 'audio' in mimetypes.guess_type(file_name)[0]
        ]
        
    def process_files(self):
        logging.info("Starting file processing")
        self.extract_audio_from_videos()
        
        music_files = self.get_music_files()
        
        for file_path in music_files:
            self.split_audio_into_chunks(file_path)

        music_files = self.get_music_files()
        
        self.delete_too_short_audios(music_files)
        
        music_files = self.get_music_files()
        
        logging.info("Found %d audio files for processing", len(music_files))
        
        self.extract_vocals(music_files, self.output_dir)
        
        if not music_files:
            logging.info("No audio files found for processing in %s", self.input_dir)
            return
        
        suffix = r'_\d{3}$'
        for file_path in music_files:
            base_name = re.sub(suffix, '', os.path.splitext(os.path.basename(file_path))[0])
            print(base_name)
            file_combined = self.combine_audio_chunks(base_name)
            if not file_combined:
                continue
            audio_output_dir = os.path.join(self.output_dir, base_name)
            os.makedirs(audio_output_dir, exist_ok=True)
            self.diarize_audio(file_combined, audio_output_dir)
            logging.info("Completed processing for %s", file_path)
        
def main(input_dir: str = AudioProcessor.DEFAULT_INPUT_DIR, 
         output_dir: str = AudioProcessor.DEFAULT_OUTPUT_DIR, 
         uvr5_model: str = AudioProcessor.DEFAULT_MODEL):
    processor = AudioProcessor(input_dir, output_dir, uvr5_model)
    processor.process_files()

if __name__ == "__main__":
    typer.run(main)

