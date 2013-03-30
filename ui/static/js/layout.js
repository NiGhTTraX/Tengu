var content, leftSidebar, rightSidebar, header, footer, resizeHandle;
var contentPaddingX, contentPaddingY;
var headerHeight, footerHeight;
var oldWindowHeight, oldWindowWidth;
var windowHeight, windowWidth;

function adjustLeftSidebar() {
	var handlePosition = resizeHandle.position().top;
	var handleHeight = resizeHandle.height();

	$("#market-tree").height(handlePosition);
	$("#items").height(leftSidebar.height() - handlePosition - handleHeight);
}

function adjustColumns() {
	var leftSidebarWidth = leftSidebar.outerWidth();
	var rightSidebarWidth = rightSidebar.outerWidth();

	leftSidebar.height(windowHeight - headerHeight - footerHeight);
	rightSidebar.height(windowHeight - headerHeight - footerHeight);

	content.width(windowWidth - leftSidebarWidth - rightSidebarWidth -
			contentPaddingX);
	content.height(windowHeight - headerHeight - footerHeight -
			contentPaddingY);

	// If the window has resized, adjust the resize handler.
	resizeHandle.css("top",
			resizeHandle.position().top - (oldWindowHeight - windowHeight) / 2);
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

	headerHeight = $("#header").outerHeight();
	footerHeight = $("#footer").outerHeight();

	contentPaddingX = content.outerWidth() - content.width();
	contentPaddingY = content.outerHeight() - content.height();

	oldWindowHeight = $(window).height();
	oldWindowWidth = $(window).width();

	adjustLayout();

	$(window).resize(function() {
		adjustLayout();
	});

	$("#resize-handle").draggable({
			axis: "y",
			containment: $("#left-sidebar"),
			drag: adjustLeftSidebar
	});
});
