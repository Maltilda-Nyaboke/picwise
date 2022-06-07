# Generated by Django 3.2 on 2022-06-07 02:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import picwise.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.UUIDField(default=uuid.UUID('ff6ed2ba-a4f3-46ab-b862-41ac03ff194e'), editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(null=True, upload_to=picwise.models.user_directory_path, verbose_name='image')),
                ('name', models.CharField(max_length=35)),
                ('caption', models.TextField()),
                ('posted', models.DateTimeField(auto_now_add=True)),
                ('likes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Tag')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stream_following', to=settings.AUTH_USER_MODEL)),
                ('image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='picwise.image')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_photo', models.ImageField(upload_to='media')),
                ('username', models.CharField(max_length=20, null=True)),
                ('bio', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='tags',
            field=models.ManyToManyField(related_name='tags', to='picwise.Tag'),
        ),
        migrations.AddField(
            model_name='image',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL)),
                ('following', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
