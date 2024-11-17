# Start with a base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy your script and requirements
COPY requirements.txt ./


# Install system dependencies
RUN apt-get update && apt-get install -y \
  gcc \
  g++ \
  libcairo2-dev \
  libffi-dev \
  build-essential \
  && apt-get clean



# copy requirements and install them
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY src/  ./src/
COPY ./config/ /default-config/
RUN ls -la /default-config


# Make entrypoint script executable
COPY entrypoint.sh  /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint and command
ENTRYPOINT ["/app/entrypoint.sh"]
