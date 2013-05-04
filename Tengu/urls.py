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
    url(r'^$', 'ui.views.home'),
    url(r'^updateWidgets/$', 'ui.views.updateWidgets'),
    url(r'^updateLeftSidebarResizeHandler/$',
        'ui.views.updateLeftSidebarResizeHandler'),
    url(r'^updateMarketTree/$', 'ui.views.updateMarketTree'),
    url(r'^getItems/(\d+)/$', 'ui.views.getItems'),
    url(r'^searchItems/(.+)/$', 'ui.views.searchItems'),
    url(r'^searchShipsAndFits/(.+)/$', 'ui.views.searchShipsAndFits'),
    url(r'^getFits/(\d+)/$', 'ui.views.getFits'),
)
