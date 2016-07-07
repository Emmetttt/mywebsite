from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

# def index(request):
#     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#     return render(request, 'home/index.html', {'posts': posts})


def index(request):
    return render(request, 'home/index.html', {})
   