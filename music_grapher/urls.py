from django.conf.urls import *

from . import views

app_name = 'music_grapher'
urlpatterns = [
    url(r'^$', views.band_input, name='index'),
    url(r'^graph/$', views.graph, name='graph'),
]

