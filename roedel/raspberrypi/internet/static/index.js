
function configure_robot_before_add(robot) {
  robot.url += '?overview=' + encodeURIComponent(document.location);
}


