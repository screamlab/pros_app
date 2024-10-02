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

cleanup() {
    echo "Shutting down docker-compose services..."
    $DOCKER_COMPOSE_COMMAND -f ./scripts/docker-compose_store_map.yml down --timeout 0 > /dev/null 2>&1
}

trap 'cleanup; exit 0' SIGINT

MAX_RETRIES=5
RETRY_COUNT=0

while true; do
    echo "Starting docker-compose services..."
    $DOCKER_COMPOSE_COMMAND -f ./scripts/docker-compose_store_map.yml up -d > /dev/null 2>&1

    echo "Monitoring logs for errors..."

    $DOCKER_COMPOSE_COMMAND -f ./scripts/docker-compose_store_map.yml logs -f | while read -r line; do
        if echo "$line" | grep -q "Failed to spin map subscription"; then
            echo "Error detected in logs: Failed to spin map subscription"

            cleanup

            ((RETRY_COUNT++))

            if [ "$RETRY_COUNT" -ge "$MAX_RETRIES" ]; then
                echo "Maximum retries reached ($MAX_RETRIES). Exiting."
                exit 1
            fi

            echo "Retrying... Attempt $RETRY_COUNT of $MAX_RETRIES"

            sleep 2

            break
        fi

        if echo "$line" | grep -q "success"; then
            echo "Success detected. Exiting."
            cleanup
            exit 0
        fi
    done

    if [ "$RETRY_COUNT" -eq 0 ]; then
        echo "No errors detected in logs. Proceeding."
        break
    fi

    if [ "$RETRY_COUNT" -lt "$MAX_RETRIES" ]; then
        continue
    fi
done

echo "Store map operation completed successfully."

echo "Press Ctrl+C to stop..."
wait
