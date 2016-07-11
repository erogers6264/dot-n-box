import random
from wordbank import words

target = random.choice(words)
attempts = input("How many attempts to guess would you like? ")
attempts_remaining = attempts

for x in xrange(1, attempts+1):
	guess = input("Please enter a single character: ").lower()
	attempts -= 1
	for i, c in enumerate(target):
		if c in target:
			pass