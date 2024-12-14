## sovits-svc-fork-uvr-env

A unified docker environment combining [SoVITS SVC fork](https://github.com/voicepaw/so-vits-svc-fork) and [UVR5](https://github.com/Anjok07/ultimatevocalremovergui).


### Prerequisites

- A Linux host system with an installed X11 display server.
- Docker daemon installed (root access may be required to access the X11 display unix socket).
- Nvidia Container Toolkit installed for GPU access.


### Installation Steps

To set up the environment, run the following command:

```bash
docker compose up -d --build
```


### Expected Runtime Behavior

Once the containers are up and running (assuming the default `docker-compose.yml` configuration):

- Two PyQT windows will appear on your host system for SoVITS-SVC and UVR5.
- The SoVITS-SVC fork will have access to the host's audio devices, allowing for real-time audio processing.
- A shared folder will be created automatically upon container startup.


### Disclaimer

This software is provided "as is," without any warranty of any kind. Use it at your own risk.

