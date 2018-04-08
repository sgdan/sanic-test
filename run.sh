#!/bin/sh

# Run in prod mode, no debug or reloading
exec docker run -it --rm --name sanic-test \
    --env-file .env \
    -p 5000:5000 \
    -v $(pwd)/.secrets:/run/secrets \
    sanic-test
