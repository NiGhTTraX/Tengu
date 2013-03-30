function updateWidgetPositions() {
	var widgetPositions = $("#stats").sortable("toArray");
	$.ajax({
			type: "GET",
			url: "/updateWidgetPositions/",
			data: {"widgetPositions": widgetPositions}
	});
}

$(document).ready(function() {
	$("#stats").sortable({
			axis: "y",
			containment: $("#right-sidebar"),
			update: updateWidgetPositions
	});

	$(".stats-widget div.toggle").disableSelection().click(function() {
		$("div.content", $(this).parent().parent()).toggle(100);
		$(this).toggleClass("collapse expand");
		return false;
	});
});
