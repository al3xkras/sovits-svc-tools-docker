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
    bash
fi
exit 0
