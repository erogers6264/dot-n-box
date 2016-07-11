import random
from wordbank import words

target = random.choice(words)
attempts = input("How many attempts to guess would you like? ")
attempts_remaining = attempts

for x in xrange(1, attempts+1):
	guess = raw_input("Please enter a single character: ")
	for i, c in enumerate(target):
		if guess == c:
			print True
		else:
			attempts -= 1
			print False