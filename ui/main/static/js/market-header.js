var searchTimer;
var oldItems = "";
var searchResults = "";

function searchItems() {
	var keywords = $.trim($("#search-items").val());
	if (keywords.length > 2) {
		$("#search div.loading").show();

		// Which tab is selected?
		var selectedTab = $("#market-tabs .current-tab").attr("id");
		var tabContents = $("#market-tree .tab-content:visible");
		var url;
		if (selectedTab == "tab-items")
			url = "/searchItems/" + keywords + "/";
		else
			url = "/searchShipsAndFits/" + keywords + "/";

		$.ajax({
				url: url,
				method: "GET",
				success: function(data) {
					$("#search div.loading").hide();
					$("#items-box").html(data);
					searchResults = data;

					// Remove selection.
					$(".market-group-name.selected", tabContents).removeClass("selected");
				}
		});
	}
}

$(document).ready(function() {
	// When switching tabs, clear the items list and the search box.
	$("#market-tabs li").click(function() {
		if ($(this).hasClass("current-tab"))
			return;

		var old = $("#items-box").html();
		$("#items-box").html(oldItems);
		oldItems = old;

	});

	// When re-focusing on the search box, display the previous seach results.
	$("#search-items").focus(function() {
		if ($(this).val() != "")
			$("#items-box").html(searchResults);
	});

	$("#search-items").bind("input", function() {
		clearTimeout(searchTimer);
		searchTimer = setTimeout(searchItems, KEY_DELAY);
	});
});

