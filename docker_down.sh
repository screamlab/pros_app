#!/bin/bash

docker stop $(docker ps -q)

docker rm $(docker ps -a -q) -f
echo All Docker Compose containers have been stopped and removed.
