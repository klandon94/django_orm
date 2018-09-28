from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^log$', views.log),
    url(r'^reg$', views.reg),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^wall$', views.wall),
    url(r'^postmsg$', views.postmsg),
    url(r'^delmsg/(?P<id>\d+)$', views.delmsg),
    url(r'^postcom/(?P<id>\d+)$', views.postcom),
    url(r'^delcom/(?P<id>\d+)$', views.delcom),
    url(r'^logout$', views.logout)
]