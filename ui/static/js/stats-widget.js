function syncPositions(that, ui) {
	// If there are more stats lists, sync their positions.
	if (!$("#stats .tab-content").size())
		return;

	// Get the original and new position of the item that was just dragged.
	var newIndex = $(ui.item).index();
	var oldIndex;
	var next = $(that).next();
	if (!next.size())
		next = $(that).prev();

	$(".stats-widget", next).each(function() {
		if ($(this).data("id") == $(ui.item).data("id")) {
			oldIndex = $(this).index();
			return false;
		}
	});

	$("#stats .tab-content").each(function() {
		if (!$(this).is(that)) {
			// Move element.
			var source = $(".stats-widget:eq(" + oldIndex + ")", $(this));
			var dest = $(".stats-widget:eq(" + newIndex + ")", $(this));
			dest.clone().insertAfter(source);
			source.clone().insertAfter(dest);
			source.remove();
			dest.remove();
		}
	});

	// Update the cookie as well.
}

function syncVisible(that) {
	var visible = $("div.content", that).is(":visible");

	$(".stats-widget").each(function() {
		if (!$(this).is(that) && $(this).data("id") == that.data("id"))
			if (visible) {
				$("div.content", this).show();
				$("div.toggle", this).toggleClass("collapse expand");
			} else {
				$("div.content", this).hide();
				$("div.toggle", this).toggleClass("collapse expand");
			}
	});
}

function updateWidgets(that) {
	/**
	 * Persist the positions and states of the stats widgets.
	 *
	 * This should be run in the context of a widget list. When updating one list,
	 * we should update all the rest to reflect the same sorting order.
	 */
	var widgets = [];
	$(".stats-widget", that).each(function() {
		widgets.push({
				name: $(this).data("id"),
				visible: $("div.content", $(this)).is(":visible")
		});
	});

	$.cookie("statsWidgets", widgets, {
			expires: COOKIE_EXPIRE,
			path: "/"
	});
}

$(document).ready(function() {
	$("#stats").on("click", ".stats-widget div.toggle", function() {
		$("div.content", $(this).parent().parent()).toggle(100, function() {
			syncVisible($(this).parent());
			updateWidgets($(this).parent().parent());
		});
		$(this).toggleClass("collapse expand");
	});

	$("#stats .tab-content").sortable({
			axis: "y",
			containment: $("#right-sidebar"),
			handle: "h1",
			update: function(e ,ui) {
				updateWidgets($(this));
				syncPositions($(this), ui);
			}
	});
});

