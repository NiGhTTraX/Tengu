// Setup CSRF protection.
var csrftoken = $.cookie("csrftoken");

function csrfSafeMethod(method) {
	// These HTTP methods do not require CSRF protection.
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var COOKIE_EXPIRE = 3600 * 24 * 30;

$.ajaxSetup({
	crossDomain: false,
	beforeSend: function(xhr, settings) {
		if (!csrfSafeMethod(settings.type)) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	}
});

// Set the jQuery cookie plugin to save content in JSON format.
$.cookie.json = true;

var KEY_DELAY = 280; // Average time between keystrokes.
