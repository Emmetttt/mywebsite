from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.utils import timezone
import re

from .models import Post
from .forms import PostForm

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date') ##-publish... reverse chrono
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_list_tag(request, **kwarg):
    unfiltered_tag = str(kwarg)
    tag = unfiltered_tag[11:-2] 
    posts = Post.objects.filter(tag=tag).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts, 'keyword' : tag})

def post_specific(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_specific.html', {'post': post})

#####Post.objects.get(pk=pk)

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_specific', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
    

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk) ####This is where we get the pk
    if request.method == "POST":
        form = PostForm(request.POST, instance=post) #####to edit
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_specific', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
