from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.display1),
    url(r'^new$', views.display2)
]