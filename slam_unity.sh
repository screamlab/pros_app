#!/bin/bash

docker-compose -f docker-compose_rplidar_unity.yml up -d
docker-compose -f docker-compose_slam_unity.yml up -d

cleanup() {
    echo "Shutting down docker-compose services..."
    docker-compose -f docker-compose_rplidar_unity.yml down
    docker-compose -f docker-compose_slam_unity.yml down
    exit 0
}

trap cleanup SIGINT

echo "Press Ctrl+C to stop..."

echo "Listening to docker-compose_slam.yml logs. Press Ctrl+C to stop..."
docker-compose -f docker-compose_slam_unity.yml logs -f &
wait