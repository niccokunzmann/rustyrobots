
# A very simple Bottle Hello World app for you to get started with...
from bottle import default_app, route, request, static_file, redirect, debug, response
import json
import os
import subprocess

server_directory = os.path.dirname(__file__)
static_directory = os.path.join(server_directory, 'static')
robots_file_path = os.path.join('/static', "robots.json")
robots_file = os.path.join(server_directory, 'static', "robots.json")

subprocess.call(['git', 'pull'], shell = True)

def load_robots():
    if not os.path.isfile(robots_file):
        return []
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
    redirect('/static/index.html')

@route('/new_robot')
def new_robot():
    response.content_type = 'text/plain; charset=UTF8'
    robots = load_robots()
    robot = dict(request.query)
    if robot not in robots:
        robots.insert(0, robot)
        result = "successfully registered:\n\t" + "\n\t".join("{}:{}".format(key, value) for key, value in sorted(robot.items()))
    else:
        result = "robot is known"
    save_robots(robots)
    return result

@route('/static/<filename:path>')
def serve_static_file(filename):
    return static_file(filename, root = static_directory)

@route('/robots')
def serve_robots():
    response.content_type = 'application/javascript'
    function = request.query.get('callback', 'robotsLoaded')
    with open(robots_file) as f:
        return "{}({})".format(function, f.read())

debug(True)

application = default_app()

