# Generated by Django 2.2.3 on 2019-07-05 06:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('contact', models.IntegerField(unique=True)),
                ('likes', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user_follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following_user', to='users.UserProfile')),
                ('user_following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_user', to='users.UserProfile')),
            ],
        ),
    ]
