#!/bin/bash

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

$DOCKER_COMPOSE_COMMAND -f ./scripts/docker-compose_ydlidar.yml up -d
$DOCKER_COMPOSE_COMMAND -f ./scripts/docker-compose_slam.yml up -d

cleanup() {
    echo "Shutting down docker-compose services..."
    docker ps -aq --filter "name=scripts*" | xargs docker rm -f
    exit 0
}

trap cleanup SIGINT

echo "Press Ctrl+C to stop..."

echo "Listening to docker-compose_slam.yml logs. Press Ctrl+C to stop..."
$DOCKER_COMPOSE_COMMAND -f ./scripts/docker-compose_slam.yml logs -f &
wait
