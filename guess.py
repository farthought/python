#!/usr/bin/python
# -*- coding: UTF-8 -*-

#This is a game, we can user it to guess the number.

import random
import gettext
guessesTaken = 0
#zh = gettext.translation('guess', localedir='./localedir', languages=['zh'])
#zh.install()

gettext.bindtextdomain('guess', "./localedir")
gettext.textdomain('guess') 
_=gettext.gettext



#print(_('Hello! What is your name?'))
#input()和raw_input:aw_input()直接读取控制台的输入
#（任何类型的输入它都可以接收）。而对于 input()，
#它希望能够读取一个合法的 python表达式，即你输入
#字符串的时候必须使用引号将它括起来，否则它会引发一个 SyntaxError 

myName = raw_input(_('Hello! What is your name?\n'))
print (_("Well, %s")) % myName
print (_("I want to play a game with you."))
print (_("I am thinking of a number between 1 and 20, then you guess."))
print (_("ok,begin."))

number = random.randint(1, 20)

while guessesTaken < 6:
    if guessesTaken == 0:
        print(_("I have already got the number, you can guess now"))
        guess = raw_input()
        guess = int(guess)
    else:
        print(_('Please try again:'))
        guess = raw_input()
        guess = int(guess)

    guessesTaken = guessesTaken +1

    if guess < number:
        print(_('Your guess is too low.'))

    if guess > number:
        print(_('Your guess is too high.'))

    if guess == number:
        break
if guess == number:
    guessesTaken = str(guessesTaken)
    print(_('Good job, %s! You guessed my number in %s guesses!') % (myName,guessesTaken))

if guess != number:
    number = str(number)
    print(_('Nope. The number I was thinking of was %s.') % (number))




