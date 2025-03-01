#!/bin/bash

docker-compose -f docker-compose.yml up --build tests --abort-on-container-exit

docker-compose -f docker-compose.yml down