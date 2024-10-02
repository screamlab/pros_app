#!/bin/bash

source "./utils.sh"
main "./scripts/docker-compose_rplidar_unity.yml" "./scripts/docker-compose_localization_unity.yml" "./scripts/docker-compose_navigation_unity.yml"
