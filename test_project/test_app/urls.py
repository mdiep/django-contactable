
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('test_app.views',
    url(r'^$',                          'person_list',      name='person_list'),
    url(r'^people/(?P<id>\d+)/?$',      'person_detail',    name='person_detail'),
    url(r'^people/(?P<id>\d+)/edit/?$', 'person_edit',      name='person_edit'),
)

