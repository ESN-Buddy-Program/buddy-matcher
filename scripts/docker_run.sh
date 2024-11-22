#!/bin/bash
# Run the Docker container
docker rm buddy-matcher 2>/dev/null || true
docker run --name buddy-matcher \
  -v "$(pwd)/config:/config" \
  -v "$(pwd)/input:/input" \
  -v "$(pwd)/output:/output" \
  daiigr/buddy-matcher:latest
