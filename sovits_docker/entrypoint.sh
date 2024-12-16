#!/bin/bash

export PULSE_SERVER=unix:${XDG_RUNTIME_DIR}/pulse/native

if [ ! "$(ls -A ~/uvr5)" ]; then
    cp -rn ~/default/uvr5/* ~/uvr5/
fi

if [ "$RUN_UVR5" = "true" ]; then
    if [ "$RUN_SOVITS_GUI" = "true" ]; then
        python ~/uvr5/UVR.py &
    else
        python ~/uvr5/UVR.py || exit 1
    fi
fi

if [ "$RUN_SOVITS_GUI" = "true" ]; then
    svcg || exit 1
else
    while true; do 
        sleep 10
    done
fi

exit 0
