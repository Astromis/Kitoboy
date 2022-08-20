#!/bin/bash

# Grant permissions to executable scripts
chmod +x -R scripts/*

# Rebuild services
sudo docker-compose down && sudo docker-compose up -d --build

# Remove <none> TAG images
docker rmi $(docker images --filter "dangling=true" -q --no-trunc)

docker exec app python3.8 db_manager.py drop_db

docker exec app python3.8 db_manager.py create_db

docker exec app ./scripts/./db_fill.sh dev