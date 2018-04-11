import asyncio
import os
import pickle
import time

import maps
from jinja2 import Environment, PackageLoader, select_autoescape
from sanic import Sanic
from sanic.response import html, json

Task = maps.namedfrozen('Task', ['name', 'start', 'duration'])
chores = ('Dishes', 'Washing', 'Ironing')

app = Sanic()
app.static('/ext', '/wserver/ext', name='ext')
app.static('/css', '/wserver/app/css', name='css')
cache = maps.NamedDict({})

# Load Jinja2 templates
env = Environment(loader=PackageLoader('Application', 'templates'),
                  autoescape=select_autoescape(['html', 'xml']),
                  enable_async=True)
home_template = env.get_template('home.html')


async def storeTotals(totals):
    pickle.dump(totals, open('totals.p', 'wb'))


async def getTotals():
    return cache.get('totals', {c: 0 for c in chores})


async def incTotal(name):
    totals = cache.get('totals', {c: 0 for c in chores})
    totals[name] = totals[name] + 1
    cache.totals = totals
    # update the file store
    asyncio.ensure_future(storeTotals(totals))


async def addTask(name, duration):
    t = Task(name, int(time.time()), duration)
    tasks = cache.get('tasks', ()) + (t,)
    cache.tasks = tasks
    asyncio.ensure_future(doTask(t))


async def doTask(task):
    # sleep for the duration of the task
    await asyncio.sleep(task.duration)

    # increment the total in the results
    await incTotal(task.name)

    # remove the task
    tasks = cache.get('tasks', ())
    tasks = tuple(t for t in tasks if t is not task)
    cache.tasks = tasks


@app.route('/')
async def home(request):
    taskname, time = tuple(request.args.get(i) for i in ('taskname', 'time'))
    if (taskname is not None and time is not None):
        await addTask(taskname, int(time))
    totals = await getTotals()
    return html(await home_template.render_async(totals=totals,
                                                 static=static,
                                                 css=css,
                                                 taskname=taskname,
                                                 time=time,
                                                 chores=chores,
                                                 eg_secret=app.config['EXAMPLE_SECRET'],
                                                 eg_env=os.environ.get('EXAMPLE_ENVIRONMENT_VARIABLE')))


@app.route('/tasks')
async def tasks(request):
    tasks = cache.get('tasks', ())
    now = int(time.time())

    def remaining(x): return x.duration - (now - x.start)
    return json(tuple({'name': t.name, 'remaining': remaining(t)} for t in tasks))


@app.route('/totals')
async def totals(request):
    return json(await getTotals())


def static(filename):
    return app.url_for('static', name='ext', filename=filename)


def css(filename):
    return app.url_for('static', name='css', filename=filename)


@app.listener('after_server_start')
async def after(app, loop):
    try:
        # Load totals and update cache
        totals = pickle.load(open('totals.p', 'rb'))
        cache.totals = totals
    except:
        print(f'Unable to load totals from file')

    # Load the example secret (docker swarm secret style)
    path = f'/run/secrets/EXAMPLE_SECRET'
    if os.path.isfile(path):
        with open(path) as f:
            app.config['EXAMPLE_SECRET'] = f.read()


if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=app.config.PORT,
            debug=app.config.DEBUG)
