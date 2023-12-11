# syntax=docker/dockerfile:1
# Built by script called build-dataloader.sh
# Run with the help of scripts in bin/ such as load-data-container.sh

# Dase image for the Docker image
FROM alpine

# Install the PostgreSQL client
RUN apk add && apk add postgresql-client

# Copy the entry point script to the root directory
COPY bin/docker-entrypoint.sh /entrypoint.sh

# Set environment variables
ENV LOUIS_DSN=
ENV LOUIS_SCHEMA=
ENV LOAD_DATA_ONLY=
ENV DISABLE_TRIGGER_ALL=
ENV DROP_SCHEMA=

# Create a volume for data storage
VOLUME /data

# Set the entry point for the container
ENTRYPOINT ["sh", "-c", "/entrypoint.sh"]
