$(document).ready(function() {
	$(".tabs li").click(function() {
		// Focus the tab.
		$(".current-tab").removeClass("current-tab");
		$(this).addClass("current-tab");

		// Display the proper content by getting the id of the element to be shown
		// from the data-id attribute.
		$(".tab-content").hide();
		$("#" + $(this).data("id")).show();
	});

	// Make the tabs sortable.
	$(".tabs ul").sortable({
			axis: "x",
			containment: $(".tabs ul"),
			delay: 150, // to prevent unwanted drags when clicking
			cursorAt: {left: 5}
	});
});

