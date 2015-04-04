

function add_headings() {
  var server = getQueryParams(document.location.search).server;
  if (server) {
    server = "?server=" + server;
  } else {
    server = "";
  }
  var parameters = {'server': server};
  var code = HEADING_TEMPLATE.formatNamed(parameters);
  var headings_div = document.createElement('div');
  headings_div.id = 'navigation';
  headings_div.innerHTML = code;
  document.body.insertBefore(headings_div, document.body.firstChild)
}

window.addEventListener('load', add_headings);

