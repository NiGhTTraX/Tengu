$(document).ready(function() {
	$("#stats").sortable({
			axis: "y",
			containment: $("#right-sidebar")
	});

	$(".stats-widget div.toggle").disableSelection().click(function() {
		$("div.content", $(this).parent().parent()).toggle(100);
		$(this).toggleClass("collapse expand");
		return false;
	});
});
