## sovits-svc-tools-docker

A unified docker environment combining [SoVITS SVC fork](https://github.com/voicepaw/so-vits-svc-fork), [UVR5](https://github.com/Anjok07/ultimatevocalremovergui), [audio-separator](https://github.com/nomadkaraoke/python-audio-separator) and [pyannote.audio](https://github.com/pyannote/pyannote-audio). 

The environment can be useful for common as well as advanced audio processing tasks involving SoVITS SVC (e.g. audio extraction, vocals extraction, speaker diarization, model training, model inference, etc), 
while keeping the environment of the host system intact. 

### Prerequisites

1. General

    - Host requirements: Nvidia Container Toolkit should be installed for GPU access.

2. To use SoVITS SVC fork or UVR5 GUI (no realtime inference): 

    - Docker host requirements: A Linux host system with an installed X11 display server.
    - Docker daemon requirements: The Docker daemon may require root access to access the X11 display unix socket.

3. To use the SoVITS SVC fork realtime inference functionality:

    - Host requirements: Pulseaudio Volume control (pulseaudio, pavucontrol) should be installed on the host system.
    

### Usage

Currently, 3 different profiles are supported, that can be used on host systems that do not meet the requirements to support the full functionality of the environment:

- CLI-only mode:

    > ./start.sh cli

- GUI mode (requirements: X11 display server):

    > ./start.sh gui
    
- GUI+realtime inference mode (requirements: X11 display server and pulseaudio volume control):

    > ./start.sh all

    
### Expected Runtime Behavior

1. CLI-only mode:

    - The container will remain idle. To use the container, run:

        > docker exec -it sovits-svc bash

2. GUI mode:

    - Two PyQT windows will appear on your host system for SoVITS-SVC and UVR5.
    - SoVITS-SVC fork will not have access to the host audio devices.

3. GUI+realtime inference:

    - Two PyQT windows will appear on your host system for SoVITS-SVC and UVR5.
    - SoVITS-SVC fork will have access to the host audio devices, allowing for real-time audio processing.


Further setup information can be found in docker-compose.yml, Dockerfile, or in individual audio processing scripts.


### Disclaimer

The software is provided "as is", without warranty of any kind. Use it at your own risk.
