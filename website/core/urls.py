from django.conf.urls import patterns, url

urlpatterns = patterns('core.views',
    url(r'^locations', 'get_locations'),
    url(r'^flag_on', 'flag_on'),
    url(r'^flag_off', 'flag_off')
    url(r'^events', 'get_events', name='get_events'),
)

