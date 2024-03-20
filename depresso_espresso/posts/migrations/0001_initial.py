# Generated by Django 5.0.2 on 2024-03-20 21:48

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(db_column='commentID', default=uuid.uuid4, primary_key=True, serialize=False)),
                ('published', models.DateTimeField(auto_now_add=True, db_column='published')),
                ('visibility', models.TextField(null=True)),
                ('contentType', models.TextField(blank=True, db_column='contentType', null=True)),
                ('comment', models.TextField()),
                ('likecount', models.IntegerField(blank=True, db_column='likeCount', default=0, null=True)),
                ('type', models.CharField(default='comment', editable=False, max_length=50)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'comments',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(db_column='postID', default=uuid.uuid4, primary_key=True, serialize=False)),
                ('source', models.TextField(blank=True, null=True)),
                ('origin', models.TextField(blank=True, null=True)),
                ('published', models.DateTimeField(blank=True, db_column='published', null=True)),
                ('visibility', models.TextField(null=True)),
                ('type', models.CharField(default='post', editable=False, max_length=50)),
                ('title', models.TextField(null=True)),
                ('description', models.TextField(null=True)),
                ('contentType', models.TextField(db_column='contentType', null=True)),
                ('content', models.TextField(db_column='content', null=True)),
                ('count', models.IntegerField(blank=True, db_column='commentCount', default=0, null=True)),
                ('likecount', models.IntegerField(blank=True, db_column='likeCount', default=0, null=True)),
                ('sharecount', models.IntegerField(blank=True, db_column='sharecount', default=0, null=True)),
                ('comments', models.URLField(blank=True, null=True)),
                ('author', models.ForeignKey(db_column='authorID', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.TextField(default='', editable=False)),
                ('author', models.JSONField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post'),
        ),
        migrations.CreateModel(
            name='LikeComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_liking_author', to=settings.AUTH_USER_MODEL)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_comment', to='posts.comment')),
            ],
            options={
                'managed': True,
                'unique_together': {('comment', 'author')},
            },
        ),
        migrations.CreateModel(
            name='LikePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_liking_author', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_post', to='posts.post')),
            ],
            options={
                'managed': True,
                'unique_together': {('post', 'author')},
            },
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sharing_author', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_post', to='posts.post')),
            ],
            options={
                'managed': True,
                'unique_together': {('post', 'author')},
            },
        ),
    ]
