from django.conf.urls import *
from . import views

app_name = 'news'
urlpatterns = [
    url(r'^$', views.news.as_view(), name='news'),
]

