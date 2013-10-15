from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'ui.main.views.home'),

    url(r'^updateLeftSidebarResizeHandler/$', 'ui.main.views.updateLeftSidebarResizeHandler'),
    url(r'^updateMarketTree/$', 'ui.market_tree.views.updateMarketTree'),
    url(r'^getItems/(\d+)/$', 'ui.items_box.views.getItems'),
    url(r'^searchItems/(.+)/$', 'ui.items_box.views.searchItems'),

    url(r'^searchShipsAndFits/(.+)/$', 'service.views.searchShipsAndFits'),
    url(r'^getFits/(\d+)/$', 'service.views.getFits'),
    url(r'^newFit/(\d+)/$', 'service.views.newFit'),
)
