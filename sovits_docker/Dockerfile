FROM pytorch/pytorch:2.5.1-cuda11.8-cudnn9-runtime

USER root

RUN apt-get update
RUN apt-get install -y git wget curl build-essential libx11-6 libasound-dev portaudio19-dev python-all-dev ffmpeg freeglut3 freeglut3-dev python3-opengl libgl1-mesa-glx libglu1-mesa

RUN useradd -m -G users sovits
WORKDIR /home/sovits

# add a .bashrc entry for docker exec ... calls
RUN echo '\nexport PATH=/home/sovits/.local/bin:$PATH' >> /home/sovits/.bashrc

USER sovits

# Thank to UVR5 for using deprecated packages
ENV SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True
ENV PATH=/home/sovits/.local/bin:$PATH
ENV HOME=/home/sovits

RUN pip install --no-cache-dir -U so-vits-svc-fork
RUN pip install --no-cache-dir --global-option='build_ext' \
    --global-option='-I/usr/local/include' \
    --global-option='-L/usr/local/lib' \
    pyaudio

RUN git clone --depth 1 https://github.com/Anjok07/ultimatevocalremovergui uvr5
RUN cd uvr5 && pip install --no-cache-dir -r requirements.txt
RUN mkdir default && cp -rf ~/uvr5 ~/default/uvr5

RUN pip install pyannote.audio typer
RUN pip install "audio-separator[gpu]" --no-deps

USER root

COPY entrypoint.sh /home/sovits
RUN chown -h sovits:sovits entrypoint.sh && chmod +x entrypoint.sh

RUN apt-get clean
RUN usermod -aG audio sovits

USER sovits

# default env
ENV RUN_SOVITS_GUI=true
ENV RUN_UVR5=false
ENV PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

CMD /home/sovits/entrypoint.sh
