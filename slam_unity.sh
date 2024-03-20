#!/bin/bash

docker-compose -f ./scripts/docker-compose_rplidar_unity.yml up -d
docker-compose -f ./scripts/docker-compose_slam_unity.yml up -d

cleanup() {
    echo "Shutting down docker-compose services..."
    docker ps -aq --filter "name=scripts*" | xargs docker rm -f
    exit 0
}

trap cleanup SIGINT

echo "Press Ctrl+C to stop..."

echo "Listening to docker-compose_slam_unity.yml logs. Press Ctrl+C to stop..."
docker-compose -f ./scripts/docker-compose_slam_unity.yml logs -f &
wait
