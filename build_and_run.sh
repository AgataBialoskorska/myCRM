#!/usr/bin/env bash

docker build . -t mycrm
echo "Docker build complete, starting container..."
docker run -d -p 8080:8080 -e SQLALCHEMY_CONFIG='mysql+pymysql://USER:PASSWORD@DATABASE_IP/DATABASE_NAME' --name mycrm mycrm
echo "Container is running, please open http://0.0.0.0:8080"