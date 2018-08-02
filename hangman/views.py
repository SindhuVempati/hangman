from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . models import Hangman
from django.db import transaction

import random
from datetime import datetime
from random import choice
import logging #TODO why is this?

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('hangman')
logger.setLevel(logging.INFO)

wordlist = []

#Loading all words from text file
def loadWords():
    with open("hangman/hangmanwords.txt") as words:
        for word in words:
            wordlist.append(word.strip().lower())

def getWord():
    if len(wordlist) == 0:
        loadWords()
        return getWord()
    else:
        random.seed(datetime.now())
        return choice(wordlist)


def home(request):
    #hangman = Hangman.objects
    return render(request, 'hangman/home.html',{'hangman': hangman})

@login_required
def hangman(request):
    if request.method == 'GET':
        word = getWord()
        hangman = Hangman(user = request.user, answer = word)
        hangman.save()
        logger.info("New Game for %s for user : " % request.user)
        hangman.image = "/static/hangme0.PNG"  #TODO set images
        hangman.display = "_ " * len(word)
        return render(request,'hangman/home.html',{'guessed':[], "hangman":hangman })
    else:
        return delegateHangman(request)


@login_required
def delegateHangman(request):
    hangman_id = int(request.POST['hangman_id'])

    hangman = Hangman.objects.get(hangman_id = hangman_id)

    if hangman.user != request.user:
        return render(request,"hangman/home.html")

    answer = hangman.answer

    guess = request.POST['buttonvalue']  #TODO button # ID
    guessed = list(hangman.guessed_word)

    if hangman.status == "win" or hangman.status == "lose":
        finishGame(hangman)
        return render(request,'hangman/home.html', {'guessed':guessed, 'hangman':hangman })
    if guess not in guessed:
        guessed.append(guess)
        hangman.guessed_word = "".join(guessed)
        hangman.save()

    wordDisplay = ""

    count = 0

    for char in answer:
        if char in guessed:
            count +=1
            wordDisplay += char + ' '
        else:
            wordDisplay += '_ '

    if count == len(answer):
        hangman.status = "win"
        hangman.save()
    hangman.display = wordDisplay

    wrongGuessCount = 0

    for char in guessed:
        if char not in answer:
            wrongGuessCount +=1

    if wrongGuessCount >= 10:
        hangman.status = 'lose'
        hangman.save()
        wrongGuessCount = 10
    hangman.image = '/static/hangme'+str(wrongGuessCount)+".PNG"

    return render(request, 'hangman/home.html', {'guessed':guessed, 'hangman':hangman } )

def finishGame(hangman):
    answer = hangman.answer
    guessed = list(hangman.guessed_word)
    if hangman.status == "win":
        hangman.display = " ".join(list(answer))
        hangman.image = '/static/hangme'+str(wrongNum(guessed,answer))+".PNG"
        return
    else:
        hangman.display = wordDisplayMeth(guessed, answer)
        hangman.image = '/static/hangme10.PNG'
        return

def wrongNum(guessed,answer):
    wrongGuessCount = 0
    for char in guessed:
        if char not in answer:
            wrongGuessCount +=1
    if wrongGuessCount >= 10:
        wrongGuessCount = 10
    return wrongGuessCount

def wordDisplayMeth(guessed, answer):
    display = ""
    count = 0
    for char in answer:
        if char in guessed:
            count += 1
            display += char + " "
        else:
            display += '_ '
    return display
