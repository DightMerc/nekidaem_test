from django.conf import settings
from django.db import models
from django.utils import timezone


# Create your models here.


class Blog(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)

    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="Подписнота")    

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    text = models.TextField()
    
    published_date = models.DateTimeField(blank=True, null=True)

    blog = models.ForeignKey(Blog, default="", on_delete=models.CASCADE)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title