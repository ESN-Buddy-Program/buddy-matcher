#!/bin/bash
# Build the Docker image
docker pull python:3.10-slim
docker build -t daiigr/buddy-matcher:latest .
