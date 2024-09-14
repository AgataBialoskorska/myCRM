#!/usr/bin/env bash

docker stop mycrm
echo "Stopping container"
docker rm mycrm
echo "Removing container"