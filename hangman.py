import random
from wordbank import words

target = random.choice(words)
attempts = input("How many attempts to guess would you like? ")
attempts_remaining = attempts


def getGuess():
	"""Request that the user enter a character
	TODO Validate the user input"""
	guess = raw_input("Please enter a single character: ")
	return guess


for x in xrange(1, attempts+1):
	for i, c in enumerate(target):
		if getGuess() == c:
			print True
		else:
			attempts -= 1
			print False