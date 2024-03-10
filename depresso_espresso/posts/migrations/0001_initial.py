# Generated by Django 5.0.2 on 2024-03-10 00:52

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
            name='Post',
            fields=[
                ('postid', models.UUIDField(db_column='postID', default=uuid.uuid4, primary_key=True, serialize=False)),
                ('authorname', models.TextField(null=True)),
                ('authorprofile', models.URLField(null=True)),
                ('title', models.TextField(null=True)),
                ('source', models.TextField(null=True)),
                ('origin', models.TextField(null=True)),
                ('description', models.TextField(null=True)),
                ('contenttype', models.TextField(db_column='contentType')),
                ('content', models.TextField(null=True)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('image_file', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('publishdate', models.DateTimeField(db_column='publishDate')),
                ('editdate', models.DateTimeField(blank=True, db_column='editDate', null=True)),
                ('visibility', models.TextField(null=True)),
                ('commentcount', models.IntegerField(blank=True, db_column='commentCount', null=True)),
                ('authorid', models.ForeignKey(db_column='authorID', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('liked_by', models.ManyToManyField(related_name='liked_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('commentid', models.UUIDField(db_column='commentID', default=uuid.uuid4, primary_key=True, serialize=False)),
                ('authorname', models.TextField(null=True)),
                ('contenttype', models.TextField(blank=True, db_column='contentType', null=True)),
                ('comment', models.TextField()),
                ('publishdate', models.DateTimeField(db_column='publishDate')),
                ('editdate', models.DateTimeField(blank=True, db_column='editDate', null=True)),
                ('commentlikecount', models.IntegerField(blank=True, db_column='commentLikeCount', null=True)),
                ('authorid', models.ForeignKey(db_column='authorID', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('liked_by', models.ManyToManyField(related_name='liked_comments', to=settings.AUTH_USER_MODEL)),
                ('postid', models.ForeignKey(db_column='postID', on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
            options={
                'db_table': 'comments',
                'managed': True,
            },
        ),
    ]
