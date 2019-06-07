#!/bin/bash

docker image prune -a -f
containers=$(docker ps -q)
docker kill $containers