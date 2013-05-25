function updateWidgets() {
	var widgets = $("#stats").sortable("toArray");
	var widgetStatuses = Array(widgets.length);

	for (var i = 0, l = widgets.length; i < l; i++) {
		widgetStatuses[i] = $("#" + widgets[i] + " div.content").is(":visible");
	}

	$.ajax({
			url: "/updateWidgets/",
			method: "POST",
			data: {
					"widgets": widgets,
					"widgetStatuses": widgetStatuses
			}
	});
}

$(document).ready(function() {
	$("#stats").sortable({
			axis: "y",
			containment: $("#right-sidebar"),
			handle: "h1",
			update: updateWidgets
	});

	$(".stats-widget div.toggle").disableSelection().click(function() {
		$("div.content", $(this).parent().parent()).toggle(100, updateWidgets);
		$(this).toggleClass("collapse expand");
	});
});
