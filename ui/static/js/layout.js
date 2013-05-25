var content, leftSidebar, rightSidebar, header, footer, resizeHandle;
var contentPaddingX, contentPaddingY;
var leftSidebarPaddingX, leftSidebarPaddingY;
var rightSidebarPaddingX, rightSidebarPaddingY;
var headerHeight, footerHeight;
var oldWindowHeight, oldWindowWidth;
var windowHeight, windowWidth;

var COOKIE_EXPIRE = 3600 * 24 * 30;


function adjustLeftSidebar() {
	var handlePosition = resizeHandle.position().top;
	var handleHeight = resizeHandle.height();

	// Adjust the resize handler.
	var distance = Math.ceil((oldWindowHeight - windowHeight) / 2);
	var top = resizeHandle.position().top;
	var oldTop = top;

	// Don't move the handler below the sidebar.
	if (top - distance >= 0)
		top -= distance;

	// Nor above it.
	if (top > leftSidebar.height())
		top = leftSidebar.height() - handleHeight;

	$("#left-sidebar-top").height(handlePosition);
	$("#left-sidebar-bottom").height(leftSidebar.height() - handlePosition - handleHeight);

	resizeHandle.css("top", top);
	if (oldTop != top)
		updateResizeHandle();
}

function updateResizeHandle() {
	var top = resizeHandle.position().top;

	$.cookie("leftSidebarResizeHandler", top, COOKIE_EXPIRE);
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
		adjustLayout();
	});

	$("#resize-handle").draggable({
			axis: "y",
			containment: $("#left-sidebar"),
			drag: adjustLeftSidebar,
			stop: updateResizeHandle
	});
});
