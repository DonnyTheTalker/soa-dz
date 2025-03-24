#!/bin/bash

docker-compose up --build tests --abort-on-container-exit

docker-compose down