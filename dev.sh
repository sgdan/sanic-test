#!/bin/sh

# Exit if there's a build error
set -e

# Build image and run in development mode
docker build . --tag sanic-test
docker run -it --rm --name sanic-test \
    --env-file .env \
    -p 5000:5000 \
    -e SANIC_DEBUG=True \
    -v $(pwd)/app:/wserver/app \
    -v $(pwd)/.secrets:/run/secrets \
    sanic-test hupper -w templates/** -w css/** -m Application

# Files in 'app' folder will be shared with container and
# automatically reloaded when they change.
