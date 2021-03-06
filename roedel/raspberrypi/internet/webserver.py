
# A very simple Bottle Hello World app for you to get started with...
from bottle import default_app, route, request, static_file, redirect, debug, response
import json
import os
import subprocess

server_directory = os.path.dirname(__file__)
static_directory = os.path.join(server_directory, 'static')
robots_file_path = os.path.join('/static', "robots.json")
robots_file = os.path.join(server_directory, 'static', "robots.json")

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

def add_robot(robot):
    robots = load_robots()
    result = robot not in robots
    if result:
        robots.insert(0, robot)
    save_robots(robots)
    return result

@route('/new_robot')
def new_robot():
    response.content_type = 'text/plain; charset=UTF8'
    if add_robot(dict(request.query)):
        return "successfully registered:\n\t" + "\n\t".join("{}:{}".format(key, value) for key, value in sorted(robot.items()))
    return "robot is known"

@route('/static/<filename:path>')
def serve_static_file(filename):
    return static_file(filename, root = static_directory)

@route('/robots')
def serve_robots():
    response.content_type = 'application/javascript; charset=UTF8'
    function = request.query.get('callback', 'robotsLoaded')
    with open(robots_file) as f:
        return "{}({})".format(function, f.read())

@route('/update')
def update():
    response.content_type = 'text/plain; charset=UTF8'
    p = subprocess.Popen(
        ['git', 'pull'],
        stdout = subprocess.PIPE, stderr = subprocess.STDOUT,
        cwd = server_directory)
    stdout, stderr = p.communicate()
    return stdout

@route('/delete_all')
def delete_all():
    save_robots([])
    return 'robots deleted'


debug(True)

application = default_app()

