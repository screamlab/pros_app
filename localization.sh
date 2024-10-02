#!/bin/bash

source "./utils.sh"
main "./scripts/docker-compose_rplidar.yml" "./scripts/docker-compose_localization.yml" "./scripts/docker-compose_navigation.yml"
