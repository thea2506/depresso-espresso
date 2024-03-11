# Generated by Django 5.0.2 on 2024-03-10 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisterConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('require_register_perms', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='author',
            name='allow_register',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
