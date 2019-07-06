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
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=100)),
                ('text', models.TextField(max_length=1000)),
                ('image', models.ImageField(upload_to=None)),
                ('link', models.URLField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('post_type', models.CharField(max_length=20)),
                ('post_topic', models.CharField(max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
