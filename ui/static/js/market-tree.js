var marketCache = {};
var searchTimer;
var SEARCH_DELAY = 280; // Average time between keystrokes

function updateMarketTree() {
	var expandedGroups = [];
	$(".market-group-name.expandable .toggle.collapse").each(function() {
		var id = parseInt($(this).parent().attr("id").substr(2));
		expandedGroups.push(id);
	});

	$.ajax({
			url: "/updateMarketTree/",
			data: {"expandedGroups": expandedGroups},
			method: "GET"
	});
}

function searchItems() {
	var keywords = $.trim($("#search-items").val());
	if (keywords.length > 2) {
		$("#search div.loading").show();
		$.ajax({
				url: "/searchItems/" + keywords + "/",
				method: "GET",
				success: function(data) {
					$("#search div.loading").hide();
					$("#left-sidebar-bottom").html(data);
				}
		});
	}
}

$(document).ready(function() {
	$(".market-group-name.expandable").click(function() {
		var nextMarketGroup = $(this).next(".market-group");
		var marketTree = $("#market-tree");
		nextMarketGroup.toggle();
		$(".toggle", this).toggleClass("expand collapse");

		// If we expanded the group, let's see if we need to scroll to it. We only
		// need to do this in case the group is taller than the container.
		if (nextMarketGroup.is(":visible")) {
			var top = $(this).offset().top - marketTree.offset().top;
			var height = top + nextMarketGroup.outerHeight() + $(this).outerHeight();
			if (height > marketTree.height())
				marketTree.scrollTop(marketTree.scrollTop() + top);
		} else {
			// We collapsed this group, so let's collapse all subgroups.
			$(".toggle.collapse", nextMarketGroup).toggleClass("expand collapse");
			$(".market-group", nextMarketGroup).hide();
		}

		updateMarketTree();
	});

	$(".market-group-name.empty").click(function() {
		var id = $(this).attr("id").substr(2);
		$(".market-group-name.selected").removeClass("selected");
		$(this).addClass("selected");

		if (marketCache[id]) {
			// Get the data from cache, saves a request.
			$("#left-sidebar-bottom").html(marketCache[id]);
		} else {
			// Request the data, then cache it.
			$.ajax({
					url: "/getItems/" + id + "/",
					method: "GET",
					success: function(data) {
						$("#left-sidebar-bottom").html(data);
						marketCache[id] = data;
					}
			});
		}
	});

	$("#search-items").focus(function() {
		if ($(this).val() == "Search term")
			$(this).val("");
	}).blur(function() {
		if ($(this).val() == "")
			$(this).val("Search term");
	});

	$("#search-items").bind("input", function() {
		clearTimeout(searchTimer);
		searchTimer = setTimeout(searchItems, SEARCH_DELAY);
	});
});

