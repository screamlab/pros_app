#!/bin/bash

docker-compose -f ./scripts/docker-compose_ydlidar.yml up -d
docker-compose -f ./scripts/docker-compose_localization.yml up -d
docker-compose -f ./scripts/docker-compose_navigation.yml up -d

cleanup() {
    echo "Shutting down docker-compose services..."
    docker ps -aq --filter "name=scripts*" | xargs docker rm -f
    exit 0
}

trap cleanup SIGINT

echo "Listening to docker-compose_navigation.yml logs. Press Ctrl+C to stop..."
docker-compose -f ./scripts/docker-compose_navigation.yml logs -f &
wait
