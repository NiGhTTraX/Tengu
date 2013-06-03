$(document).ready(function() {
	$(document).on("click", ".tabs li:not(.current-tab)", function() {
		var parent = $(this).parent();

		// Focus the tab.
		$(".current-tab", parent).removeClass("current-tab");
		$(this).addClass("current-tab");

		/**
		 * If the ul element has a data-id attribute, then whenever a tab is
		 * selected, all the divs that have the class tab-content in the element
		 * whose id is set through data-id will be hidden. Then, the element whose
		 * id is set through the data-id attribute belonging to the selected tab
		 * will be shown.
		 */
		if (parent.data("id")) {
			$(".tab-content", $("#" + parent.data("id"))).hide();
			$("#" + $(this).data("id")).show();
		}
	});

	// Handle the close tab button.
	$(document).on("click", ".tabs li .close", function() {
		var parent = $(this).parent();
		var list = parent.parent();

		// Remove the tab and the tab content.
		$("#" + parent.data("id")).remove();
		parent.remove();

		// Refresh the list.
		list.sortable("refresh");

		// Focus on right most tab.
		var last = $("li:not(.static):last", list);
		if (last.size()) {
			last.addClass("current-tab");
			$("#" + last.data("id")).show();
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

