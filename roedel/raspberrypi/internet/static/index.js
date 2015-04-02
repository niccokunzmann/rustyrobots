function add_robot(index) {
  robot = robots[index];
  var exampleEntry = document.getElementById('exampleEntry');
  html = exampleEntry.innerHTML;
  robot.index = index + "";
  robot.url += '?overview=' + encodeURIComponent(document.location);
  var htmlsave_robot = {};
  var keys = Object.keys(robot);
  for (var i = 0; i < keys.length; i++) {
    htmlsave_robot[keys[i]] = robot[keys[i]].HTMLescape();
  }
  html = html.formatNamed(htmlsave_robot);
  document.getElementById('listRobots').innerHTML += html;
}
