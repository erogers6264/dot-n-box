import random
from wordbank import words

target = random.choice(words)
attempts = input("How many attempts to guess would you like? ")
attempts_remaining = attempts

for x in xrange(1, attempts+1):
	guess = input("Please guess a single letter: ").lower()
	attempts =- 1
	for c in target:
		if guess in list(target.split()):
			pass

