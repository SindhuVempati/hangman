# Generated by Django 2.0.2 on 2018-07-29 00:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hangman', '0002_auto_20180728_2045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hangman',
            name='playtime',
        ),
    ]