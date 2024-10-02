#!/bin/bash

SCRIPT="./scripts/docker-compose_dabai_camera.yml"

cleanup() {
    local script="$1"
    echo "Shutting down docker compose services..."
    $DOCKER_COMPOSE_COMMAND -f $script down --timeout 0
    exit 0
}

main() {
    local script="$1"
    # Determine which docker compose command to use
    if command -v docker-compose &> /dev/null
    then
        DOCKER_COMPOSE_COMMAND="docker-compose"
    elif docker compose version &> /dev/null
    then
        DOCKER_COMPOSE_COMMAND="docker compose"
    else
        echo "Neither 'docker-compose' nor 'docker compose' is installed. Please install Docker Compose."
        exit 1
    fi

    $DOCKER_COMPOSE_COMMAND -f $script up -d

    trap "cleanup $script" SIGINT

    echo "Press Ctrl+C to stop..."

    echo "Listening to docker-compose_camera.yml logs. Press Ctrl+C to stop..."
    $DOCKER_COMPOSE_COMMAND -f $script logs -f &
    wait
}

main $SCRIPT
