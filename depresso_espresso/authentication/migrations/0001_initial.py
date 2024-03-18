# Generated by Django 5.0.2 on 2024-03-18 02:41

import django.contrib.auth.models
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requester', models.CharField(max_length=200)),
                ('receiver', models.CharField(max_length=200)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ourUsername', models.CharField(max_length=50)),
                ('ourPassword', models.CharField(max_length=50)),
                ('theirUsername', models.CharField(max_length=50)),
                ('theirPassword', models.CharField(max_length=50)),
                ('baseUrl', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='RegisterConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requireRegisterPerms', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(db_column='authorID', default=uuid.uuid4, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('host', models.URLField(blank=True, null=True)),
                ('type', models.CharField(default='author', max_length=50)),
                ('displayName', models.CharField(max_length=50)),
                ('github', models.URLField(blank=True, null=True)),
                ('profileImage', models.URLField(blank=True, null=True)),
                ('allowRegister', models.BooleanField(default=False)),
                ('isExternalAuthor', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authorid', models.CharField(max_length=200)),
                ('followingid', models.CharField(max_length=200)),
                ('areFriends', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'managed': True,
                'unique_together': {('authorid', 'followingid')},
            },
        ),
    ]