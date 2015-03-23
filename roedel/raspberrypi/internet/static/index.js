
function getQueryParams(qs) {
    // from http://stackoverflow.com/a/1099670/1320237
    qs = qs.split("+").join(" ");

    var params = {}, tokens,
        re = /[?&]?([^=]+)=([^&]*)/g;

    while (tokens = re.exec(qs)) {
        params[decodeURIComponent(tokens[1])]
            = decodeURIComponent(tokens[2]);
    }

    return params;
}

function get_robots_url() {
  var params = getQueryParams(document.location.search);
  if (params.server == null) {
    params.server = 'rustyrobots.pythonanywhere.com';
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
    add_robot(robot, i);
  }
}

function add_robot(robot, index) {
  var exampleEntry = document.getElementById('exampleEntry');
  html = exampleEntry.innerHTML;
  robot.index = index;
  html = html.formatNamed(robot);
  document.getElementById('listRobots').innerHTML += html;
}

if (!String.prototype.formatNamed) {
  // First, checks if it isn't implemented yet.
  // http://stackoverflow.com/a/4673436/1320237
  String.prototype.formatNamed = function(key_value_pairs) {
    return this.replace(/\{([^}]+)\}/g, function(match, name) { 
      value = key_value_pairs[name];
      if (typeof value != 'undefined') {
        return value;
      }
      return match;
    });
  };
}

window.addEventListener('load', load_robots);




