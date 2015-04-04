
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
  if (params.overview == null) {
    params.overview = DEFAULT_ROBOTS_SERVER;
  }
  return 'http://' + params.overview + "/robots";
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


String.prototype.HTMLescape = function() {
  // from
  //   http://stackoverflow.com/a/5499821/1320237
  var tagsToReplace = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;'
  };
  return this.replace(/[&<>]/g, function(tag) {
    return tagsToReplace[tag] || tag;
  });
};


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



