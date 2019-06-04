#!/bin/bash

docker system prune -af
cd ~/Repos/core
script/dev_env --build --gui