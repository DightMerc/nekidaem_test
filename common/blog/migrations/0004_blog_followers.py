# Generated by Django 2.2.2 on 2019-06-05 06:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0003_auto_20190604_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='Подписнота', to=settings.AUTH_USER_MODEL),
        ),
    ]