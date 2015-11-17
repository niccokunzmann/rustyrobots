idw.bookmark={};


$(document).ready(function() {
    var ud_dict = {
        'item_type': idw_current_document_type,
        'item_id': idw_current_document_id,
        'lang': idw_lang
    }
    
    $.post("/objects/" + 'bookmark' + "/check_if_bookmarked", JSON.stringify(ud_dict), idw.bookmark.show_icon, "json");
    
});


idw.bookmark.show_icon = function(data_in) {
    var data = data_in['data']['formdata'];
    var icon_title, icon_status, icon_link, icon_style;
    
    if (data == 0) {
	// is NOT bookmarked
	icon_status = "bookmark not_bookmarked ";
	icon_style = "";
	icon_link = "javascript: idw.bookmark.toggle('bookmark')";
	
	if (idw_lang == "de_DE") {
	    icon_title = "auf Merkliste übernehmen";
	}
	if (idw_lang == "en_US") {
	    icon_title = "bookmark";
	}
    }
    if (data == 1) {
	// is bookmarked
	icon_status = "bookmark bookmarked ";
	icon_style = "";
	icon_link = "javascript: idw.bookmark.toggle('unbookmark')";
	
	if (idw_lang == "de_DE") {
	    icon_title = "von Merkliste entfernen";
	}
	if (idw_lang == "en_US") {
	    icon_title = "unbookmark";
	}
    }
    
    $("#bookmark_icon").html("<span style=\"display: inline-block;\" class=\"icon " + icon_status + "medium\" data-icon=\"b\" title=\"" + icon_title + "\"><span aria-hidden=\"true\"><a styĺe=\"" + icon_style + "\" href=\"" + icon_link + "\">b</a></span></span>");
}


idw.bookmark.toggle = function(mode) {
    var ud_dict = {
        'item_type': idw_current_document_type,
        'item_id': idw_current_document_id,
        'lang': idw_lang
    }
    
    if (mode == "bookmark") {
	//code
	$.post("/objects/" + 'bookmark' + "/do_bookmark", JSON.stringify(ud_dict), idw.bookmark.show_icon, "json");
    }
    if (mode == "unbookmark") {
	//code
	$.post("/objects/" + 'bookmark' + "/do_unbookmark", JSON.stringify(ud_dict), idw.bookmark.show_icon, "json");
    }
}
