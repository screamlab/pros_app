#!/bin/bash

source "./utils.sh"
main "./scripts/docker-compose_ydlidar.yml" "./scripts/docker-compose_localization.yml" "./scripts/docker-compose_navigation.yml"
