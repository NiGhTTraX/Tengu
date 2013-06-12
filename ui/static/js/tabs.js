function focusTab(tab) {
	/**
	 * Switches to a tab.
	 *
	 * Args:
	 *	tab: Can either be an id (including the leading '#') or a jQuery element.
	 *
	 * Returns:
	 *	True: If the tab exists.
	 *	False: If there is no such tab.
	 */
	var o = $(tab);

	if (o.size()) {
		var list = o.parent();
		var pane = $(list.data("id"));

		$(".current-tab", list).removeClass("current-tab");
		$(".tab-content", pane).hide();
		o.addClass("current-tab");
		$(o.data("id")).show();

		return true;
	}

	return false;
}

/**
 * Closes a tab.
 *
 * This removes the tab element from the DOM of the containing list and
 * refreshes the sortable plugin. The current focus is moved to the right most
 * tab, if one exists.
 *
 * At the end, it triggers a 'tabs.close' event that can be picked up by the
 * apropriate handlers.
 *
 * Args:
 *	that: jQuery object representing the tab to be closed.
 */
function closeTab(that) {
	var list = that.parent();

	// Remove the tab and the tab content. See below for more details on data
	// attributes.
	var obj = that.data("obj");
	if (obj)
		obj.remove();
	else
		$(that.data("id")).remove();
	that.remove();

	// Refresh the list.
	list.sortable("refresh");

	// Focus on right most tab.
	var last = $("li:not(.static):last", list);
	if (last.size()) {
		last.addClass("current-tab");
		$(last.data("id")).show();
	}

	list.trigger("tabs.close");
}

$(document).ready(function() {
	$(document).on("click", ".tabs li:not(.current-tab)", function() {
		var parent = $(this).parent();

		// Focus the tab.
		$(".current-tab", parent).removeClass("current-tab");
		$(this).addClass("current-tab");

		/**
		 * If the ul element has a data-id attribute, then whenever a tab is
		 * selected, all the divs that have the class tab-content in the element
		 * whose id is set through data-id will be hidden. Then, if an element is set
		 * through data-obj or an id of an element is set through data-id, that
		 * element is shown. data-obj takes priority over data-id.
		 */
		var pid = parent.data("id");
		if (pid) {
			$(".tab-content", $(pid)).hide();

			var obj = $(this).data("obj");
			if (obj)
				obj.show();
			else
				$($(this).data("id")).show();
		}
	});

	// Handle the close tab button.
	$(document).on("click", ".tabs li .close", function() {
		closeTab($(this).parent());
	});

	// Close tabs on middle button.
	$(document).on("mousedown", ".tabs li:not(.static)", function(e) {
		if (e.which == 2) {
			// Only sortable tabs may be closed.
			if ($(this).parent().parent().hasClass("sortable"))
				closeTab($(this));
		}
	});


	// Make the tabs sortable.
	$(".tabs.sortable ul").sortable({
			items: "> li:not(.static)",
			axis: "x",
			containment: "parent",
			delay: 150, // to prevent unwanted drags when clicking
			cursorAt: {left: 5}
	});
});

