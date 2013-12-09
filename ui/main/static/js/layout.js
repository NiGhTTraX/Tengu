var content, leftSidebar, rightSidebar, header, footer, resizeHandle;
var contentPaddingX, contentPaddingY;
var leftSidebarWidth, rightSidebarWidth;
var leftSidebarPaddingX, leftSidebarPaddingY;
var rightSidebarPaddingX, rightSidebarPaddingY;
var handleHight;
var headerHeight, footerHeight;
var oldWindowHeight, oldWindowWidth;
var containerHeight, containerWidth;
var containment = [0, 0, 0, 0];
var resizeHandleTopLimit;

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

function adjustResizeHandle() {
	/**
	* Adjust the resize handle's position when the container's height changes.
	*/
	var top = resizeHandle.position().top;
	var oldTop = top;

	var direction = oldWindowHeight < containerHeight ? -1 : 1;
	var distance = Math.floor(
			Math.abs(oldWindowHeight - containerHeight) / 2) * direction;

	// Adjust the resize handler, only if the container has changed.
	if (distance) {
		// Don't move the handler below the containment.
		if (top - distance >= resizeHandleTopLimit)
			top -= distance;
		else
			top = resizeHandleTopLimit;

		/**
		* There shouldn't be any case in which the handler would go over the bottom
		* limit because it only moves 1/2 of the container difference, so the container
		* will advance faster than it. Thus, no need to check for the bottom limit.
		*/
	}

	// Update the position and adjust the left sidebar.
	if (oldTop != top) {
		resizeHandle.css("top", top);
		adjustLeftSidebar();
	}
}

function updateResizeHandle() {
	/**
	* Store the resize handle position in a cookie.
	*/
	var top = resizeHandle.position().top;

	$.cookie("leftSidebarResizeHandler", top, {
			expires: COOKIE_EXPIRE,
			path: "/"
	});
}

function adjustLeftSidebar() {
	/**
	* Resize the top and bottom portions of the left sidebar so they fill the
	* column's height.
	*/
	var handlePosition = resizeHandle.position().top;

	$("#left-sidebar-top").height(handlePosition);
	$("#left-sidebar-bottom").height(leftSidebar.height() - handlePosition - handleHeight);

}

function adjustColumns() {
	/**
	* Resizes the 3 columns so they fill the entire container.
	*/
	leftSidebar.height(containerHeight - headerHeight - footerHeight -
			leftSidebarPaddingY);
	rightSidebar.height(containerHeight - headerHeight - footerHeight -
			rightSidebarPaddingY);

	content.width(containerWidth - leftSidebarWidth - rightSidebarWidth -
			contentPaddingX);
	content.height(containerHeight - headerHeight - footerHeight -
			contentPaddingY);
}

function adjustLayout() {
	// Get the new container's dimmensions.
	containerWidth = $("#container").width();
	containerHeight = $("#container").height();

	// Adjust layout.
	adjustColumns();
	calculateContainment();
	adjustResizeHandle();

	// Store the container's dimmensions.
	oldWindowWidth = containerWidth;
	oldWindowHeight = containerHeight;
}


$(document).ready(function() {
	// Get some objects and and properties that will never change.
	content = $("#content");
	leftSidebar = $("#left-sidebar");
	rightSidebar = $("#right-sidebar");
	resizeHandle = $("#resize-handle");

	handleHeight = resizeHandle.outerHeight(true);

	headerHeight = $("#header").outerHeight(true);
	footerHeight = $("#footer").outerHeight(true);

	contentPaddingX = content.outerWidth(true) - content.width();
	contentPaddingY = content.outerHeight(true) - content.height();

	leftSidebarWidth = leftSidebar.outerWidth(true);
	rightSidebarWidth = rightSidebar.outerWidth(true);
	leftSidebarPaddingX = leftSidebar.outerWidth(true) - leftSidebar.width();
	leftSidebarPaddingY = leftSidebar.outerHeight(true) - leftSidebar.height();
	rightSidebarPaddingX = rightSidebar.outerWidth(true) - rightSidebar.width();
	rightSidebarPaddingY = rightSidebar.outerHeight(true) - rightSidebar.height();

	var search = $("#search");
	resizeHandleTopLimit = search.position().top + search.outerHeight(true);

	oldWindowHeight = containerHeight = $(container).height();
	oldWindowWidth = containerWidth = $(container).width();

	adjustColumns();
	calculateContainment();

	// Restore resize handler's position.
	var top = $.cookie("leftSidebarResizeHandler");
	if (top) {
		resizeHandle.css("top", parseInt(top));
	} else {
		// Adjust the resize handle to be at 50% height.
		resizeHandle.css("top", Math.floor(leftSidebar.height() / 2));
	}

	adjustLeftSidebar();

	$(window).resize(function() {
		adjustLayout();
		updateResizeHandle();
	});

	$("#resize-handle").draggable({
			axis: "y",
			containment: containment,
			drag: adjustLeftSidebar,
			stop: updateResizeHandle
	});
});

