from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
	url(r'^[a-zA-Z_]+$', views.redirect),
]