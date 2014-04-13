EXPANDED_GROUPS_COOKIE = "expanded_groups";

var itemsCache = {};


function updateMarketTree() {
	var expandedGroups = [];
	$(".market-group-name.expandable .toggle.collapse").each(function() {
		var id = parseInt($(this).parent().attr("id").substr(2));
		expandedGroups.push(id);
	});

	$.cookie(EXPANDED_GROUPS_COOKIE, expandedGroups);
}

function toggleMarketGroup(group) {
	var nextMarketGroup = $(group).next(".market-group");
	var marketTree = $("#market-tree");
	nextMarketGroup.toggle();
	$(".toggle", group).toggleClass("expand collapse");

	// If we expanded the group, let's see if we need to scroll to it. We only
	// need to do it in case the group is taller than the container.
	if (nextMarketGroup.is(":visible")) {
		var top = $(group).offset().top - marketTree.offset().top;
		var height = top + nextMarketGroup.outerHeight() + $(group).outerHeight();
		if (height > marketTree.height())
			marketTree.scrollTop(marketTree.scrollTop() + top);
	} else {
		// We expanded this group, so let's collapse all subgroups.
		$(".toggle.collapse", nextMarketGroup).toggleClass("expand collapse");
		$(".market-group", nextMarketGroup).hide();
	}
}

$(document).ready(function() {
	// Let's expand the groups, if necessary.
	var expandedGroups = $.cookie(EXPANDED_GROUPS_COOKIE);
	if (expandedGroups) {
		$.each(expandedGroups, function() {
			var group = $("#mg" + this);
			toggleMarketGroup(group);
		});
	}

	$(".market-group-name.expandable").click(function() {
		toggleMarketGroup(this);
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

