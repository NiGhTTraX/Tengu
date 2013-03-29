var content, leftSidebar, rightSidebar, header, footer;
var contentPaddingX, contentPaddingY;
var headerHeight, footerHeight;

function adjustLayout() {
	var windowWidth = $(this).width();
	var windowHeight = $(this).height();

	var leftSidebarWidth = left_sidebar.outerWidth();
	var rightSidebarWidth = right_sidebar.outerWidth();

	console.log(leftSidebarWidth + " " + rightSidebarWidth);
	console.log(windowWidth + " " + contentPaddingX);

	left_sidebar.height(windowHeight - headerHeight - footerHeight);
	right_sidebar.height(windowHeight - headerHeight - footerHeight);

	content.width(windowWidth - leftSidebarWidth - rightSidebarWidth -
			contentPaddingX);
	content.height(windowHeight - headerHeight - footerHeight -
			contentPaddingY);
}

$(window).ready(function() {
	content = $("#content");
	left_sidebar = $("#left-sidebar");
	right_sidebar = $("#right-sidebar");

	headerHeight = $("#header").outerHeight();
	footerHeight = $("#footer").outerHeight();

	contentPaddingX = content.outerWidth() - content.width();
	contentPaddingY = content.outerHeight() - content.height();

	adjustLayout();

	$(window).resize(function() {
		adjustLayout();
	});
});

