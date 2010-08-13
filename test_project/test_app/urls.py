
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('test_app.views',
    url(r'^$',                          'person_list',      name='person_list'),
)

