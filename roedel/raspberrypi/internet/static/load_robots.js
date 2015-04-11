
function get_robots_url() {
  var params = getQueryParams(document.location.search);
  if (params.server == null) {
    params.server = document.location.protocol == 'file:' ? 
                      DEFAULT_ROBOTS_SERVER_ON_FILE_SYSTEM : 
                      DEFAULT_ROBOTS_SERVER;
  }
  return params.server + "/robots";
}

var robots = [];

function load_robots() {
  var script = document.createElement('script');
  script.src = get_robots_url();
  document.head.appendChild(script)
}

function robotsLoaded(new_robots) {
  for (var i = 0; i < new_robots.length; i++) {
    check_robot(new_robots[i]);
  }
}

function check_robot(robot) {
  if (robot.information_javascript) {
    var script = document.createElement('script');
    script.src = robot.information_javascript;
    document.head.appendChild(script);
  } 
}

function add_robot(index) {
  var robot = robots[index];
  if (robot.added) {
    return;
  }
  robot.added = true;
  robot.index = index + "";
  if (configure_robot_before_add) {
    configure_robot_before_add(robot);
  }
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

function add_robot_information(robot) {
  for (var i = 0; i < robots.length; i++) {
    if (robots[i].id == robot.id) {
      return;
    }    
  }
  robots.push(robot);
  add_robot(robots.indexOf(robot));
}

window.addEventListener('load', load_robots);




