from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('iphonefood_core.views',
    url(r'^dishes/$', 'dishes', name='dishes'),
    url(r'^addresses/$', 'addresses', name='addresses'),
    url(r'^top/$', 'top', name='top'),
)
