from django.shortcuts import render, get_object_or_404
from .models import Blog, Post
from .forms import PostForm
from django.shortcuts import redirect
from django.utils import timezone


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()

            post.blog = Blog.objects.get(owner=request.user)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            
            post.blog = Blog.objects.get(owner=request.user)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def blog_list(request):
    user = request.user
    blogs = Blog.objects.all()
    posts = Post.objects.all()
    try:
        choosen_blog = get_object_or_404(Blog, id=request.GET.get('q',''))
    except:
        pass

    
    subscribed = []
    

    if request.method == "POST":
        for checked_user in choosen_blog.followers.all():
            subscribed.append(checked_user.id)

        if user.id in subscribed:
            choosen_blog.followers.remove(request.user.id)
        else:
            choosen_blog.followers.add(request.user.id)

    return render(request, 'blog/blog_list.html', {'blogs': blogs, 'user': user})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    user = request.user.id

    follow = []
    for follower in blog.followers.all():
        follow.append(follower.id)
        
    subscribed = False
    blogs = Blog.objects.filter(followers__id=user)
    posts = Post.objects.all()
    current_blog_records = posts.filter(blog__id=blog.id)


    if request.method == "POST":

        if user in follow:
            

            full_records_ids = []

            for record in current_blog_records:
                full_records_ids.append(record.pk)

            checked_posts = Post.objects.filter(pk__in=full_records_ids)

            for checked_post in checked_posts:
                checked_post.seen_by.remove(request.user.id)

            blog.followers.remove(request.user.id)
            
        else:
            blog.followers.add(request.user.id)
            subscribed = True
    else:

        if user in follow:
            subscribed = True

    return render(request, 'blog/blog_detail.html', {'blog': blog, 'subscribed': subscribed, 'posts': current_blog_records, 'user': request.user})

def wall(request):
    user = request.user
    blogs = Blog.objects.filter(followers__id=user.id)
    posts = Post.objects.all()
    try:
        checked_post = get_object_or_404(Post, id=request.GET.get('q',''))
    except:
        pass

    
    seen = []
    

    if request.method == "POST":
        for checked_user in checked_post.seen_by.all():
            seen.append(checked_user.id)

        if user.id in seen:
            checked_post.seen_by.remove(request.user.id)
        else:
            checked_post.seen_by.add(request.user.id)

    full_records_ids = []
    for blog in blogs:
        current_blog_records = posts.filter(blog__id=blog.id)
        for record in current_blog_records:
            full_records_ids.append(record.pk)
    sorted_posts = Post.objects.filter(pk__in=full_records_ids).order_by('-published_date')

    return render(request, 'blog/wall.html', {'posts': sorted_posts, 'user': user})
    