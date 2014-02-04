function adjustResizeHandle(data) {
	var resizeHandle = $("#resize-handle"),
			handleHeight = resizeHandle.outerHeight(true),
			top = resizeHandle.position().top,
			oldTop = top,
			direction = data.oldWindow.height < data.window.height ? 1 : -1,
			distance = Math.floor(
					Math.abs(data.oldWindow.height - data.window.height) / 2) * direction,
			updateTimeout;

	// Adjust the resize handler, only if the container height has changed.
	if (distance) {
		top += distance;

		// Don't move the handler above the containment.
		if (top < 0)
			top = 0;

		/**
		* There shouldn't be any case in which the handler would go over the bottom
		* limit because it only moves 1/2 of the container difference, so the container
		* will advance faster than it. Thus, no need to check for the bottom limit.
		*/
	}

	// Update the position and adjust the left sidebar.
	if (oldTop !== top) {
		clearTimeout(updateTimeout);
		updateTimeout = setTimeout(function() {
			updateResizeHandle();
		}, 100);
		resizeHandle.css("top", top);

		resizeLeftSidebar();
	}
}

function resizeLeftSidebar() {
	var top = $("#resize-handle").position().top,
			height = $("#containment").height(),
			handleHeight = $("#resize-handle").outerHeight(true);

	$("#market-tree").css("bottom", height - top);
	$("#items-box").css("top", top + handleHeight);
}

function updateResizeHandle() {
	/**
	* Store the resize handle position in a cookie.
	*/
	var top = $("#resize-handle").position().top;

	$.cookie("leftSidebarResizeHandle", top, {
			expires: COOKIE_EXPIRE,
			path: "/"
	});
}

$(document).ready(function() {
	var oldWindowHeight = $(window).height(),
			oldWindowWidth = $(window).width(),
			resizeHandle = $("#resize-handle"),
			data;

	// Restore resize handle's position.
	var top = $.cookie("leftSidebarResizeHandle");
	if (top && top >=0 && top <= $("#containment").height()) {
		resizeHandle.css("top", parseInt(top));
	} else {
		// Adjust the resize handle to be at 50% height.
		resizeHandle.css("top", Math.floor($("#containment").height() / 2));
	}
	resizeLeftSidebar();

	// When the window resizes, adjust the resize handle and the left sidebar.
	$(window).resize(function() {
		data = {
			oldWindow: {
				height: oldWindowHeight,
				width: oldWindowWidth
			},
			window: {
				height: $(this).height(),
				width: $(this).width
			}
		};
		oldWindowHeight = $(this).height();
		oldWindowWidth = $(this).width();

		adjustResizeHandle(data);
	});

	$("#resize-handle").draggable({
			axis: "y",
			containment: "#containment",
			drag: resizeLeftSidebar,
			stop: updateResizeHandle
	});
});

