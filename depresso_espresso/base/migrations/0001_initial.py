# Generated by Django 5.0.2 on 2024-02-28 11:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Following',
            fields=[
                ('authorid', models.TextField(db_column='authorID', primary_key=True, serialize=False)),
                ('followerid', models.TextField(db_column='followerID')),
            ],
            options={
                'db_table': 'following',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('authorid', models.OneToOneField(db_column='authorID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'likes',
                'managed': False,
            },
        ),
    ]
