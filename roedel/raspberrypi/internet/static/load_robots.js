
function get_robots_url() {
  var params = getQueryParams(document.location.search);
  if (params.server == null) {
    params.server= DEFAULT_ROBOTS_SERVER;
  }
  return 'http://' + params.server + "/robots";
}

var robots = [];

function load_robots() {
  var script = document.createElement('script');
  script.src = get_robots_url();
  document.head.appendChild(script)
}

function robotsLoaded(new_robots) {
  robots = new_robots;
  for (var i = 0; i < robots.length; i+= 1) {
    robot = robots[i];
    check_robot(robot, i);
  }
}

function check_robot(robot, index) {
  if (robot.echo == null) return;
  url = robot.echo + '?content=add_robot(' + index + ')';
  var script = document.createElement('script');
  script.src = url;
  document.head.appendChild(script);
}

function add_robot(index) {
  var robot = robots[index];
  if (robot.added) {
    return;
  }
  robot.added = true;
  robot.index = index + "";
  configure_robot_before_add(robot);
  var exampleEntry = document.getElementById('exampleEntry');
  html = exampleEntry.innerHTML;
  var htmlsave_robot = {};
  var keys = Object.keys(robot);
  for (var i = 0; i < keys.length; i++) {
    htmlsave_robot[keys[i]] = (robot[keys[i]] + '').HTMLescape();
  }
  html = html.formatNamed(htmlsave_robot);
  document.getElementById('listRobots').innerHTML += html;
}

window.addEventListener('load', load_robots);




