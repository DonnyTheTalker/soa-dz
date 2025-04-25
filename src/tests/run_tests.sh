#!/bin/bash

podman-compose up --build tests --abort-on-container-exit

podman-compose down