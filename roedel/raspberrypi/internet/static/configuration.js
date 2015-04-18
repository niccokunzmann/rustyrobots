
function configure_robot_before_add(robot) {
  robot.is_selected = false;
  robot.toggleRobot = "javascript:toggleRobot(" + robot.index + ")";
  robot.robotLinkId = "robotEntry_" + robot.index;
}

function toggleRobot(index) {
  var robot = robots[index];
  robot.is_selected = !robot.is_selected;
  robotLink = document.getElementById(robot.robotLinkId);
  if (robot.is_selected && !robotLink.classList.contains("selectedRobot")) {
    robotLink.classList.add("selectedRobot");
  } else {
    robotLink.classList.remove("selectedRobot");
  }
}

function get_selected_robots() {
  var selected_robots = [];
  for (var i = 0; i < robots.length; i++) {
    var robot = robots[i];
    if (robot.is_selected) {
      selected_robots.push(robot);
    }
  }
  return selected_robots;
}

var callback_number = 0;

function get_callback_function_name(callback_function) {
  if (window[callback_function.name] === callback_function) {
    return callback_function.name;
  }
  while (true) {
    callback_number++;
    var callback_name = 'callback_' + callback_number;
    if (!window[callback_name]) {
      window[callback_name] = callback_function;
      return callback_name;
    }
  }
}

function parameters_to_query(parameters) {
  var query = "";
  var parameter_names = Object.keys(parameters);
  for (var i = 0; i < parameter_names.length; i++) {
    var parameter_name = parameter_names[i];
    var parameter_value = parameters[parameter_name];
    if (query == "") {
      query += "?";
    } else {
      query += '&';
    }
    query += encodeURIComponent(parameter_name) + '=' + encodeURIComponent(parameter_value + '');
  }
  return query;
}

function get_robot_callback_function_name(robot, callback) {
  return get_callback_function_name(function () {
    // http://javascript.info/tutorial/arguments
    var args = [].slice.call(arguments)
    args.unshift(robot);
    callback.apply(window, args);
  })
}

function default_robot_callback(robot, message, description) {
  alert(robot.name + ': ' + message + "\n" + description);
}


function execute_path_on_selected_robots(attribute, parameters, callback) {
  var selected_robots = get_selected_robots();
  if (!callback) {
    callback = default_robot_callback;
  }
  for (var i = 0; i < selected_robots.length; i++) {
    var robot = selected_robots[i];
    var call_url = robot[attribute];
    if (call_url) {
      parameters.callback_function = get_robot_callback_function_name(robot, callback);
      call_url += parameters_to_query(parameters);
      var script = document.createElement('script');
      script.src = call_url;
      document.body.appendChild(script);
    } else {
      callback(robot, 'error', attribute + ' was not registered as a command.');
    }
  }
}

function formatted_robot_names() {
  var selected_robots = get_selected_robots();
  if (selected_robots.length == 0) {
    return "";
  } else if (selected_robots.length == 1) {
    return selected_robots[0].name + "";
  } 
  var s = "";
  for (var i = 0; i < selected_robots.length - 2; i++) {
    s += selected_robots[i].name + ", ";
  }
  s += selected_robots[selected_robots.length - 2].name + ' and ' + 
       selected_robots[selected_robots.length - 1].name;
  return s;
}

function add_wifi_robot() {
  var arguments = {
    "ssid": document.getElementById('wifi_ssid').value,
    "password": document.getElementById('wifi_password').value,
  };
  execute_path_on_selected_robots('add_wifi', arguments);
}

function remove_wifi_robot() {
  var arguments = {
    "ssid": document.getElementById('wifi_ssid').value,
  };
  execute_path_on_selected_robots('remove_wifi', arguments);
}

function restart_robot() {
  execute_path_on_selected_robots('restart', {});
}

function shutdown_robot() {
  if (!get_selected_robots().length) {
    return;
  }
  if (confirm("Really shutdown " + formatted_robot_names() + "?")) {
    execute_path_on_selected_robots('shutdown', {});
  }
}

function update_robot() {
  execute_path_on_selected_robots('update', {});
}

function rename_robot() {
  var parameters = {
    "hostname" : document.getElementById('robot_hostname').value
  };
  execute_path_on_selected_robots('rename', parameters);
}

function set_robot_image() {
  var parameters = {
    "image_url" : document.getElementById('robot_image').value
  };
  execute_path_on_selected_robots('set_image_url', parameters);
}

function refresh_preview_image() {
  document.getElementById('preview_image').src = document.getElementById('robot_image').value;
}

function mark_configuration_options() {
  var options = document.getElementsByClassName("configurationOption");
  for (var i = 0; i < options.length; i++) {
    options[i].classList.add(i & 1 ? "even" : "odd");
  }
}

window.addEventListener('load', mark_configuration_options);
window.addEventListener('load', refresh_preview_image);


