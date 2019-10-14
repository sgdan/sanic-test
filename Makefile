.build: Dockerfile
	docker build -t sanic-test .
	touch .build

# Build image and run in dev mode
# Files in 'app' folder will be shared with container and
# automatically reloaded when they change
dev: .build
	docker-compose run \
		-p 5000:5000 \
		sanic-test hupper -w templates/** -w css/** -m Application
