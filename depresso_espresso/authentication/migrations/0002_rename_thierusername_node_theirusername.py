# Generated by Django 5.0.2 on 2024-03-15 04:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='node',
            old_name='thierUsername',
            new_name='theirUsername',
        ),
    ]
