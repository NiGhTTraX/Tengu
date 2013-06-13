from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Tengu.views.home', name='home'),
    # url(r'^Tengu/', include('Tengu.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'ui.views.index.home'),
    url(r'^updateWidgets/$', 'ui.views.ajax.updateWidgets'),
    url(r'^updateLeftSidebarResizeHandler/$',
        'ui.views.ajax.updateLeftSidebarResizeHandler'),
    url(r'^updateMarketTree/$', 'ui.views.ajax.updateMarketTree'),
    url(r'^getItems/(\d+)/$', 'ui.views.ajax.getItems'),
    url(r'^searchItems/(.+)/$', 'ui.views.ajax.searchItems'),
    url(r'^searchShipsAndFits/(.+)/$', 'service.views.ajax.searchShipsAndFits'),
    url(r'^getFits/(\d+)/$', 'service.views.ajax.getFits'),
    url(r'^newFit/(\d+)/$', 'service.views.ajax.newFit'),
    url(r'^fit/([0-9a-zA-z]+)/$', 'ui.views.index.home'),
    url(r'^getFit/([0-9a-zA-z]+)/$', 'service.views.ajax.getFit'),
)
