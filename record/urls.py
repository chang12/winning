from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cancel/$', views.match_cancel, name='match_cancel'),
    url(r'^detail/(?P<pk1>\d+)/(?P<pk2>\d+)/$', views.detail, name='detail'),
    url(r'^find/(?P<mode>\w+)/$', views.find, name='find'),
    url(r'^new/$', views.match_new, name='match_new'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^show/$', views.match_show, name='match_show'),
]
