from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^confirm/(?P<token>[a-z0-z\-]+)/$', views.confirm, name='confirm'),
]
