
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

