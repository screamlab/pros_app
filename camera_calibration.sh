#!/bin/bash

# 設置校準參數
export SIZE="6x9"
export SQUARE="0.025"
export IMAGE_TOPIC="/camera/color/image_raw"
export CAMERA_NAME="/my_camera"

source "./utils.sh"
main "./docker/compose/docker-compose_camera_calibration.yml"
