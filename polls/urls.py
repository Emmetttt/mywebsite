from django.conf.urls import patterns, include, url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create/$', views.CreatePageView.as_view(), name='create'),
    url(r'^test/$', views.test.as_view(), name='test'),
    url(r'^test2/$', views.test2.as_view(), name='test2'),
    url(r'^(?P<pk>[0-9]+)/$', views.PollDetailsPageView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsPageView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]


    # url(r'^(?P<pk>[^/]+)/create/$', views.CreateView.as_view(), name='create'),
