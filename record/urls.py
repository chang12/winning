from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.match_new, name='match_new'),
    url(r'^find/$', views.find, name='find'),
    url(r'^detail/(?P<pk1>\d+)/(?P<pk2>\d+)/$', views.detail, name='detail'),
]
