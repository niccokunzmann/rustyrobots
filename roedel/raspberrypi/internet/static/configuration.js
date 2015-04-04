
function configure_robot_before_add(robot) {
  robot.chosen = false;
  robot.toggleRobot = "javascript:toggleRobot(" + robot.index + ")";
  robot.robotLinkId = "robotEntry_" + robot.index;
}

function toggleRobot(index) {
  var robot = robots[index];
  robot.chosen = !robot.chosen;
  robotLink = document.getElementById(robot.robotLinkId);
  if (robot.chosen && !robotLink.classList.contains("selectedRobot")) {
    robotLink.classList.add("selectedRobot");
  } else {
    robotLink.classList.remove("selectedRobot");
  }
}
