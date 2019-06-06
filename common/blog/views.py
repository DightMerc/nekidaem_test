from django.shortcuts import render, get_object_or_404
from .models import Blog, Post

# Create your views here.
def blog_list(request):
    return render(request, 'blog/blog_list.html', {})

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    user = request.user.id

    follow = []
    for follower in blog.followers.all():
        follow.append(follower.id)
        
    subscribed = False

    if request.method == "POST":

        if user in follow:
            blog.followers.remove(request.user.id)
        else:
            blog.followers.add(request.user.id)
            subscribed = True
    else:

        if user in follow:
            subscribed = True

    return render(request, 'blog/blog_detail.html', {'blog': blog, 'subscribed': subscribed})

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
    sorted_posts = Post.objects.filter(pk__in=full_records_ids).filter().order_by('-published_date')

    return render(request, 'blog/wall.html', {'posts': sorted_posts, 'user': user})
    