#!/bin/bash

#builds and runs the docker container
bash scripts/init_dev_env.sh
bash scripts/docker_build.sh
bash scripts/docker_run.sh
