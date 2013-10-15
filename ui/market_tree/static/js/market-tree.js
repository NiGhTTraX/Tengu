var itemsCache = {};

function updateMarketTree() {
	var expandedGroups = [];
	$(".market-group-name.expandable .toggle.collapse").each(function() {
		var id = parseInt($(this).parent().attr("id").substr(2));
		expandedGroups.push(id);
	});

	$.ajax({
			url: "/updateMarketTree/",
			method: "POST",
			data: {"expandedGroups": expandedGroups}
	});
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
		var selectedTab = $("#market-tabs .current-tab").attr("id");

		$(".market-group-name.selected:visible").removeClass("selected");
		$(this).addClass("selected");

		// Is this an item group, or a ship?
		if (selectedTab == "tab-items") {
			if (itemsCache[id]) {
				// Get the data from cache, saves a request.
				$("#items-box").html(itemsCache[id]);
			} else {
				// Request the data, then cache it.
				$.ajax({
						url: "/getItems/" + id + "/",
						method: "GET",
						success: function(data) {
							$("#items-box").html(data);
							itemsCache[id] = data;
						}
				});
			}
		}
		else if (selectedTab == "tab-ships") {
			// Responses can not be cached since they're always changing.
			$.ajax({
					url: "/getFits/" + id + "/",
					method: "GET",
					success: function(data) {
						$("#items-box").html(data);
					}
			});
		}
	});
});

