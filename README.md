## sovits-svc-tools-docker

A unified docker environment combining [SoVITS SVC fork](https://github.com/voicepaw/so-vits-svc-fork), [UVR5](https://github.com/Anjok07/ultimatevocalremovergui), [audio-separator](https://github.com/nomadkaraoke/python-audio-separator) and [pyannote.audio](https://github.com/pyannote/pyannote-audio). 
Additionally provides audio processing scripts 

### Prerequisites

1. General

    - Docker daemon installed.
    - Nvidia Container Toolkit installed for GPU access.

2. To use SoVITS SVC fork or UVR5 GUI: 

    - A Linux host system with an installed X11 display server.
    - Docker daemon may require root access to access the X11 display unix socket.


### Installation Steps

```bash
docker compose up -d --build
```


### Expected Runtime Behavior

1. If GUI is enabled in the `docker-compose.yml` (assuming the default configuration):

    - Two PyQT windows will appear on your host system for SoVITS-SVC and UVR5.
    - The SoVITS-SVC fork will have access to the host's audio devices, allowing for real-time audio processing.
    - A shared folder will be created automatically upon container startup.

2. Otherwise, the container will be accessible by docker exec:

    ```docker exec -it sovits-svc bash```


For more detailed information, check docker-compose.yml, Dockerfile or a specific script that you're interested in.


### Disclaimer

This software is provided "as is", without warranty of any kind. Use it at your own risk.

