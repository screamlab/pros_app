#!/bin/bash

docker-compose -f ./scripts/docker-compose_rplidar_unity.yml up -d
docker-compose -f ./scripts/docker-compose_localization_unity.yml up -d
docker-compose -f ./scripts/docker-compose_navigation_unity.yml up -d

cleanup() {
    echo "Shutting down docker-compose services..."
    docker-compose -f ./scripts/docker-compose_rplidar_unity.yml down
    docker-compose -f ./scripts/docker-compose_localization_unity.yml down
    docker-compose -f ./scripts/docker-compose_navigation_unity.yml up down
    exit 0
}

trap cleanup SIGINT

echo "Listening to docker-compose_navigation.yml logs. Press Ctrl+C to stop..."
docker-compose -f ./scripts/docker-compose_navigation.yml logs -f &
wait
