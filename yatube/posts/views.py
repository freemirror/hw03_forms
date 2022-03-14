from django.shortcuts import render, get_object_or_404
from .models import Post, Group
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import datetime

User = get_user_model()


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    author = User.objects.get(username=username)
    posts = Post.objects.filter(author=author.id).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = Post.objects.filter(author=author.id).count
    context = {
        'page_obj': page_obj,
        'author': author,
        'count': count
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    posts = Post.objects.get(id=post_id)
    count = Post.objects.filter(author=posts.author).count
    context = {
        'posts': posts,
        'count': count,
    }
    return render(request, template, context)


@login_required()
def post_create(request):
    template = 'posts/create_post.html'
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            print(request)
            return redirect('posts:profile', request.user.username)
        return render(request, template, {'form': form})
    form = PostForm()
    return render(request, template, {'form': form})


@login_required()
def post_edit(request, post_id):
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.pub_date = datetime.datetime.now()
                post.save()
                return redirect('posts:post_detail', post_id)
        else:
            form = PostForm(instance=post)
    else:
        return redirect('posts:post_detail', post_id)
    return render(request, template, {'form': form, 'is_edit': True})
