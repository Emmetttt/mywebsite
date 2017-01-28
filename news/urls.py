from django.conf.urls import patterns, include, url

from . import views

app_name = 'news'
urlpatterns = [
    url(r'^$', views.news, name='news'),
]

