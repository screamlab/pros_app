#!/bin/bash

docker-compose -f ./scripts/docker-compose_store_map.yml up -d

cleanup() {
    echo "Shutting down docker-compose services..."
    docker-compose -f ./scripts/docker-compose_store_map.yml down
    exit 0
}

trap cleanup SIGINT

echo "Press Ctrl+C to stop..."

echo "Listening to docker-compose_store_map.yml logs. Press Ctrl+C to stop..."
docker-compose -f ./scripts/docker-compose_store_map.yml logs -f &
wait
