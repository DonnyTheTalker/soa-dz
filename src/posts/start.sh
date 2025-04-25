#!/usr/bin/env bash

./wait-for-it.sh zookeeper:2181
./wait-for-it.sh kafka:9092
./wait-for-it.sh db:5432

python main.py