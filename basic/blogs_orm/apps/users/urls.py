from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register$', views.display1),
    url(r'^login$', views.display2),
    url(r'^users/new$', views.display1),
    url(r'^users$', views.display3)
]