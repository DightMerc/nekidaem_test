from django.shortcuts import render, get_object_or_404
from .models import Blog

# Create your views here.
def blog_list(request):
    return render(request, 'blog/blog_list.html', {})

def blog_detail(request, pk):
    if request.method == "POST":
        blog = get_object_or_404(Blog, pk=pk)
        user = request.user.id

        follow = []
        for follower in blog.followers.all():
            follow.append(follower.id)

        subscribed = False

        if user in follow:
            blog.followers.remove(request.user.id)
        else:
            blog.followers.add(request.user.id)
            subscribed = True

        return render(request, 'blog/blog_detail.html', {'blog': blog, 'subscribed': subscribed})
    else:
        blog = get_object_or_404(Blog, pk=pk)
        user = request.user.id

        follow = []
        for follower in blog.followers.all():
            follow.append(follower.id)
            
        subscribed = False

        if user in follow:
            subscribed = True



        return render(request, 'blog/blog_detail.html', {'blog': blog, 'subscribed': subscribed})