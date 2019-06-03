#!/bin/bash

docker system prune -a -f
cd ~/Repos/core
script/dev_env --build --gui