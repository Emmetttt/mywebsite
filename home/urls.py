from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'home', views.index, name='index'),
    url(r'links', views.links, name='links'),
    url(r'maths', views.maths, name='maths'),
    url(r'about', views.about, name='about'),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
