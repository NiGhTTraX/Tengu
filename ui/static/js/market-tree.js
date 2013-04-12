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
		}

		updateMarketTree();
	});

	$(".market-group-name.empty").click(function() {
		$(".market-group-name.selected").removeClass("selected");
		$(this).addClass("selected");
	});
});

