docker run -it --rm \
    -v "$(pwd)/src:/workspaces/src" \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --network compose_my_bridge_network \
    --env-file ./.env \
    ghcr.io/otischung/pros_ai_image_pybullet:latest \
    /bin/bash