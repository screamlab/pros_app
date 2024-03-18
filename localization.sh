#!/bin/bash

docker-compose -f ./scripts/docker-compose_rplidar.yml up -d
docker-compose -f ./scripts/docker-compose_localization.yml up -d
docker-compose -f ./scripts/docker-compose_navigation.yml up -d

cleanup() {
    echo "Shutting down docker-compose services..."
    docker-compose -f ./scripts/docker-compose_rplidar.yml down
    docker-compose -f ./scripts/docker-compose_localization.yml down
    docker-compose -f ./scripts/docker-compose_navigation.yml up down
    exit 0
}

trap cleanup SIGINT

echo "Listening to docker-compose_navigation.yml logs. Press Ctrl+C to stop..."
docker-compose -f ./scripts/docker-compose_navigation.yml logs -f &
wait
