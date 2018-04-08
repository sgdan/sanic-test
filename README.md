# sanic-test
This is a very simple webapp that uses the [Sanic](https://github.com/channelcat/sanic/)
web framework. It implements a number of features (see below) but only to a hello-world level.
Sanic supports concurrency by using the [uvloop](https://github.com/MagicStack/uvloop) event loop
implementation of Python3's [asyncio](https://github.com/python/cpython/tree/3.6/Lib/asyncio/).
This means you can take advantage of async/await style code from Python 3.5+ which is a coroutine
approach within a single process (rather than a multi-process approach).

See the [dev.sh] script which can be used to build and run in debug mode. After running
the script, go to http://localhost:5000 to see the app. By default it runs in debug mode
and reloads whenever source files are changed. There's also a [run.sh] script showing how
it can be run without the reloading.

## Features
The following features are implemented to hello-world level, just to see them working:
- Reloading using [Hupper](https://github.com/Pylons/hupper) for debug mode
- Based on [Python3/Alpine docker image](https://github.com/docker-library/python/blob/e48c9718ef52d14df2ac46e674b0fb55523d8284/3.6/alpine3.7/Dockerfile)
- NamedDict and namedfrozen collections from [maps](https://github.com/pcattori/maps)
- [Pickle](https://wiki.python.org/moin/UsingPickle) to persist the task totals to file
- Bootstrap 4 template based on the [Sticky footer navbar](https://getbootstrap.com/docs/4.0/examples/)
  example.
- Loads an example docker swarm style secret via `/run/secrets/EXAMPLE_SECRET`. In a real project
  it would not be checked into the repository as this example is! See [.secrets/EXAMPLE_SECRET](.secrets/EXAMPLE_SECRET)
- [Jinja2](http://jinja.pocoo.org/docs/2.10/) to render the main page and the two JSON endpoints (see http://localhost:5000/tasks and http://localhost:5000/totals)
