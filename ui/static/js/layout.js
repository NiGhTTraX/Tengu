var content, leftSidebar, rightSidebar, header, footer, resizeHandle;
var contentPaddingX, contentPaddingY;
var leftSidebarPaddingX, leftSidebarPaddingY;
var rightSidebarPaddingX, rightSidebarPaddingY;
var headerHeight, footerHeight;
var oldWindowHeight, oldWindowWidth;
var windowHeight, windowWidth;

function adjustLeftSidebar() {
	var handlePosition = resizeHandle.position().top;
	var handleHeight = resizeHandle.height();

	// Adjust the resize handler.
	var distance = Math.ceil((oldWindowHeight - windowHeight) / 2);
	var top = resizeHandle.position().top;
	if (top - distance >= 0)
		top -= distance;
	if (top > leftSidebar.height())
		top = leftSidebar.height() - handleHeight;

	$("#market-tree").height(handlePosition);
	$("#items").height(leftSidebar.height() - handlePosition - handleHeight);

	resizeHandle.css("top", top);
	updateResizeHandle();
}

function updateResizeHandle() {
	var top = resizeHandle.position().top;

	$.ajax({
			url: "/updateLeftSidebarResizeHandler/",
			method: "GET",
			data: {"top": top}
	});
}

function adjustColumns() {
	var leftSidebarWidth = leftSidebar.outerWidth();
	var rightSidebarWidth = rightSidebar.outerWidth();

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

	headerHeight = $("#header").outerHeight();
	footerHeight = $("#footer").outerHeight();

	contentPaddingX = content.outerWidth() - content.width();
	contentPaddingY = content.outerHeight() - content.height();

	leftSidebarPaddingX = leftSidebar.outerWidth() - leftSidebar.width();
	leftSidebarPaddingY = leftSidebar.outerHeight() - leftSidebar.height();
	rightSidebarPaddingX = rightSidebar.outerWidth() - rightSidebar.width();
	rightSidebarPaddingY = rightSidebar.outerHeight() - rightSidebar.height();

	oldWindowHeight = $(window).height();
	oldWindowWidth = $(window).width();

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
