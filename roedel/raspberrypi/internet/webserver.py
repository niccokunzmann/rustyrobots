
# A very simple Bottle Hello World app for you to get started with...
from bottle import default_app, route, request, static_file, redirect
import json
import os

server_directory = os.path.dirname(__file__)
static_directory = os.path.join(server_directory, 'static')
robots_file = os.path.join(static_directory, "robots.json")

def load_robots():
    with open(robots_file) as f:
        try:
            return json.load(f)
        except:
            return []

def save_robots(robots):
    with open(robots_file, 'w') as f:
        return json.dump(robots, f)

@route('/')
def hello_world():
    redirect('/static')

@route('/new_robot')
def new_robot():
    robots = load_robots()
    robot = dict(request.query)
    if robot not in robots:
        robots.insert(0, robot)
    save_robots(robots)

@route('/static/<filename:path>')
def serve_static_file(filename):
    return static_file(filename, root = static_directory)


application = default_app()

