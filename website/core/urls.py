from django.conf.urls import patterns, url

urlpatterns = patterns('core.views',
    url(r'^locations', 'get_locations'),
)
