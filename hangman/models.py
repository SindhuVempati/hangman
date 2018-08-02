from __future__ import unicode_literals
#http://python-future.org/unicode_literals.html
from django.db import models
from django.contrib.auth.models import User


class Hangman(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    hangman_id = models.AutoField(primary_key = True)
    answer = models.CharField(max_length = 25)
    guessed_word = models.CharField(max_length = 15, default = "")
    status = models.CharField(max_length = 10, default = "ongoing")
    wins_total = models.IntegerField(default = 0)
    losses_total = models.IntegerField(default = 0)


    def __unicode__(self):
        return "To be filled"
