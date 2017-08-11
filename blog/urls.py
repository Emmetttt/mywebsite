from django.shortcuts import render
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^filter/(?P<kwarg>[\w\-]+)/$', views.post_list_tag, name='post_list_tag'),
    url(r'^post/(?P<pk>\d+)/$', views.post_specific, name='post_specific'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]