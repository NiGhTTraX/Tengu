var content, leftSidebar, rightSidebar, header, footer, resizeHandle;
var contentPaddingX, contentPaddingY;
var leftSidebarPaddingX, leftSidebarPaddingY;
var rightSidebarPaddingX, rightSidebarPaddingY;
var handleHight;
var headerHeight, footerHeight;
var oldWindowHeight, oldWindowWidth;
var windowHeight, windowWidth;
var containment = [0, 0, 0, 0];

var COOKIE_EXPIRE = 3600 * 24 * 30;


function calculateContainment() {
	/**
	 * Calculates the bounding box for the resize handler.
	 *
	 * Update the elements directly so jQuery UI will use the new box. If we were
	 * to just assign containment a new array, this would create a new object and
	 * jQuery UI would still be using the old one.
	 */
	var marketTree = $("#market-tree");
	containment[0] = marketTree.offset().left;
	containment[1] = marketTree.offset().top;
	containment[2] = leftSidebar.offset().left + leftSidebar.width();
	containment[3] = leftSidebar.offset().top + leftSidebar.height() -
					resizeHandle.outerHeight(true);
}

function adjustLeftSidebar() {
	var handlePosition = resizeHandle.position().top;
	var distance = Math.floor((oldWindowHeight - windowHeight) / 2);
	var top = resizeHandle.position().top;
	var oldTop = top;

	// Adjust the resize handler, only if the window has changed.
	if (distance) {
		// Don't move the handler below the containment.
		if (top - distance >= containment[1])
			top -= distance;

		// Nor above it.
		if (top > containment[3])
			top = containment[3];
	}

	$("#left-sidebar-top").height(handlePosition);
	$("#left-sidebar-bottom").height(leftSidebar.height() - handlePosition - handleHeight);

	resizeHandle.css("top", top);
	if (oldTop != top)
		updateResizeHandle();
}

function updateResizeHandle() {
	var top = resizeHandle.position().top;

	$.cookie("leftSidebarResizeHandler", top, {
			expires: COOKIE_EXPIRE,
			path: "/"
	});
}

function adjustColumns() {
	var leftSidebarWidth = leftSidebar.outerWidth(true);
	var rightSidebarWidth = rightSidebar.outerWidth(true);

	leftSidebar.height(windowHeight - headerHeight - footerHeight -
			leftSidebarPaddingY);
	rightSidebar.height(windowHeight - headerHeight - footerHeight -
			rightSidebarPaddingY);

	content.width(windowWidth - leftSidebarWidth - rightSidebarWidth -
			contentPaddingX);
	content.height(windowHeight - headerHeight - footerHeight -
			contentPaddingY);
}

function adjustLayout() {
	windowWidth = $(window).width();
	windowHeight = $(window).height();

	adjustColumns();
	adjustLeftSidebar();

	oldWindowWidth = windowWidth;
	oldWindowHeight = windowHeight;
}

$(document).ready(function() {
	content = $("#content");
	leftSidebar = $("#left-sidebar");
	rightSidebar = $("#right-sidebar");
	resizeHandle = $("#resize-handle");

	handleHeight = resizeHandle.outerHeight(true);

	headerHeight = $("#header").outerHeight(true);
	footerHeight = $("#footer").outerHeight(true);

	contentPaddingX = content.outerWidth(true) - content.width();
	contentPaddingY = content.outerHeight(true) - content.height();

	leftSidebarPaddingX = leftSidebar.outerWidth(true) - leftSidebar.width();
	leftSidebarPaddingY = leftSidebar.outerHeight(true) - leftSidebar.height();
	rightSidebarPaddingX = rightSidebar.outerWidth(true) - rightSidebar.width();
	rightSidebarPaddingY = rightSidebar.outerHeight(true) - rightSidebar.height();

	oldWindowHeight = $(window).height();
	oldWindowWidth = $(window).width();

	// Restore resize handler's position.
	var top = $.cookie("leftSidebarResizeHandler");
	if (top)
		resizeHandle.css("top", parseInt(top));

	adjustLayout();

	$(window).resize(function() {
		calculateContainment();
		adjustLayout();
	});

	calculateContainment();

	$("#resize-handle").draggable({
			axis: "y",
			containment: containment,
			drag: adjustLeftSidebar,
			stop: updateResizeHandle
	});

	$.cookie.json = true;
});
