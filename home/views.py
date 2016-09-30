from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

def index(request):
    return render(request, 'home/index.html', {})

def links(request):
    return render(request, 'home/links.html', {})
   