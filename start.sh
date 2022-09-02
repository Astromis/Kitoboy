#!/bin/bash

# Grant permissions to executable scripts
chmod +x -R scripts/*

# Rebuild services
sudo docker-compose down && sudo docker-compose up -d --build

# Remove <none> TAG images
docker rmi $(docker images --filter "dangling=true" -q --no-trunc)

# Drop existing db
docker exec app python3.8 db_manager.py drop_db

# Create fresh db
docker exec app python3.8 db_manager.py create_db


# Fill db with dump data
docker exec app ./scripts/./db_fill.sh dev