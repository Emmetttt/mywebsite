from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Post

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date') ##TEST THIS IN SHELL THO
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': Post})

#####Post.objects.get(pk=pk)
