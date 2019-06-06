from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail

from django.dispatch import receiver
from django.db.models.signals import post_save


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

    seen_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="Глянули")  

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title



@receiver(post_save, sender=Post)
def my_handler(sender, created, instance, **kwargs):
    if created:
        post_id = instance.id
        followers =  instance.blog.followers.all()
        email_addresses = []
        for follower in followers:
            email_addresses.append(follower.email)
            text = 'Новый пост на вашей стене. 127.0.0.1:8000/post/{}/'.format(str(instance.id))
            send_mail(
                        'Новый пост',
                        text,
                        'dightmerc@gmail.com',
                        email_addresses,
                        fail_silently=False,
                    )