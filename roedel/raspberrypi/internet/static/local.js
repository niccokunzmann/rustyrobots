
function shutdown_server() {
  var script = document.createElement('script');
  script.src = "/shutdown";
  document.body.appendChild(script);
}

function shutdown_successful() {
  window.close();
}

function add_addresses(links) {
  var linkElement = document.getElementById('listUrls');
  for (var i = 0; i < links.length; i++) {
    var link = links[i];
    linkElement.innerHTML += '<a target="_blank" href="' + encodeURI(link) + '">' + link + "</a><br/>";
  }
}

function load_links() {
  var script = document.createElement('script');
  script.src = "/addresses";
  document.body.appendChild(script);
}

window.addEventListener('load', load_links);
