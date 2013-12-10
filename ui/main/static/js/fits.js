function loadFit(data, tab, fit, stats) {
	var name = data["shipName"];
	var fitID = data["fitID"];
	var fitURL = data["fitURL"];

	$(".title", tab).text(name);
	tab.removeData("obj");
	tab.data("id", "#fit" + fitID + ", #stats" + fitID);
	tab.data("fitID", fitID);
	tab.data("url", fitURL);
	tab.attr("id", "fit-tab" + fitID);

	fit.attr("id", "fit" + fitID);
	fit.removeClass("vcw");
	fit.html(data["render"]);

	// Initialize the fitting wheel.
	$(".fittingWheel", fit).wheel();

	// Change the URL.
	window.history.replaceState({"fitID": fitID}, "", "/fit/" + fitURL + "/");

	// TODO: Refresh the left sidebar.
}

function newTab() {
	// Remove the welcome tab, but store it in case we ever need it later.
	$("#tabs-fits li.welcome").hide();

	// Create a new tab.
	$("#tabs-fits .current-tab").removeClass("current-tab");

	var title = $("<div></div>").text("Loading...").addClass("title");
	var close = $("<div></div>").addClass("close");
	var tab = $("<li></li>").append(title).append(close);
	tab.addClass("current-tab");

	// Prepare the loader.
	var loaderContent = $("<div></div>").addClass("vcc");
	var loaderText = $("<div></div>").addClass("vct");
	var loader = $("<div></div>").addClass("loader");
	loaderText.append(loader);
	loaderContent.append(loaderText);

	// Create a new fitting window.
	$("#fitting-window .tab-content").hide();
	var fit = $("<div></div>").append(loaderContent);
	fit.addClass("tab-content vcw");

	// Create a new stats list.
	/*
	$("#stats .tab-content").hide();
	var stats = $("<div></div>").append(loaderContent.clone());
	stats.addClass("tab-content vcw");
	*/

	tab.data("obj", $([fit, stats]));
	$("#tabs-fits").append(tab);
	$("#tabs-fits").sortable("refresh");
	$("#fitting-window").append(fit);
	//$("#stats").append(stats);

	return {"tab": tab, "fit": fit};//, "stats": stats};
}

function newFit(id) {
	var r = newTab();

	$.ajax({
		url: "/newFit/" + id + "/",
		method: "POST",
		dataType: "json",
		success: function(data) { loadFit(data, r.tab, r.fit);}//, r.stats); }
	});
}


$(document).ready(function() {
	// Attach handlers to create new fit links.
	$(document).on("click", ".fit-new", function() {
		var id = $(this).data("id");
		newFit(id);
	});

	$(document).on("click", ".fit-link", function() {
		var fitID = $(this).data("id");

		// Only create a new tab if there isn't already one. If there is one, switch
		// to it.
		if (!focusTab("#fit-tab" + fitID)) {
			var r = newTab();
			$.ajax({
					url: "/getFit/" + fitID + "/",
					success: function(data) {
						loadFit(data, r.tab, r.fit, r.stats);
					}
			});
		} else {
			// Get fit URL and update the browser URL.
			var fitURL = $("#fit-tab" + fitID).data("url");
			window.history.replaceState({"fitID": fitID}, "", "/fit/" + fitURL + "/");
		}
	});

	// Prevent the welcome tab button from bubbling up.
	$("#tabs-fits li.welcome").on("click mousedown", function(e) {
		e.stopImmediatePropagation();
	});

	// Freeze the welcome tab.
	$("#tabs-fits li.welcome").addClass("static");
	$("#tabs-fits").sortable("refresh");

	/**
	 * If the last tab is closed, show the tip.
	 *
	 * Make sure to include the tabs script file before this one, or else this
	 * handler will be executed before the one in that file. Since the tabs
	 * framework is responsible for removing the DOM element, our handler won't do
	 * anything because the list won't be empty.
	 */
	$(document).on("tabs.close", "#tabs-fits", function() {
		var last = $("li:not(.static):visible", $("#tabs-fits"));
		if (!last.size()) {
			$("#tabs-fits li.welcome").show().addClass("current-tab");
			$("#fitting-window .tab-content.tip").show();
			window.history.replaceState(undefined, "", "/");
		}
	});

	// Manage history states.
	$("#tabs-fits").on("click", "li:not(.current-tab)", function() {
		var fitID = $(this).data("fitID");
		if (fitID) {
			var fitURL = $(this).data("url");

			window.history.replaceState({"fitID": fitID}, "", "/fit/" + fitURL + "/");
		}
	});

	window.onpopstate = function(e) {
		if (!e.state)
			return;

		if (!focusTab("#fit-tab" + e.state.fitID))
			window.history.replaceState(undefined, "", "/");
	};
});

