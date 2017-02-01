from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from .models import News
from .forms import NewsForm

class news(generic.ListView):
	template_name = 'news/news.html'
	context_object_name = 'news_list'

	def get_queryset(self):
		return News.objects.all()