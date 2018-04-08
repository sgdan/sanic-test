FROM python:3.6.5-alpine3.7

# For example of how to add sanic to alpine see:
# https://hub.docker.com/r/ubergarm/sanic-alpine/~/dockerfile/
RUN apk add --no-cache build-base \
    && pip3 install --no-cache-dir sanic hupper jinja2 maps \
    && apk del build-base

RUN mkdir -p /wserver/ext && cd /wserver/ext \
    && wget -q https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css \
    && wget -q https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js \
    && wget -q https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js \
    && wget -q https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js

# Create user and folder for server files
RUN adduser -D wserver wserver
COPY app/Application.py /wserver/app/
COPY app/templates/*.html /wserver/app/templates/
COPY app/css/*.css /wserver/app/css/
RUN chown -R wserver:wserver /wserver

USER wserver
WORKDIR /wserver/app
ENV SANIC_PORT 5000
ENV SANIC_DEBUG False
EXPOSE 5000
CMD ["python3", "Application.py"]
