#!/bin/bash

docker-compose -f docker-compose_rplidar_unity.yml up -d
docker-compose -f docker-compose_localization_unity.yml up -d
docker-compose -f docker-compose_navigation.yml up -d

cleanup() {
    echo "Shutting down docker-compose services..."
    docker-compose -f docker-compose_rplidar_unity.yml down
    docker-compose -f docker-compose_localization_unity.yml down
    docker-compose -f docker-compose_navigation.yml up down
    exit 0
}


trap cleanup SIGINT

echo "Listening to docker-compose_navigation.yml logs. Press Ctrl+C to stop..."
docker-compose -f docker-compose_navigation.yml logs -f &
wait