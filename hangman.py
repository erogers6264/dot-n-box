from wordbank import randomWord


def startGame():
	attempts = input("How many attempts to guess would you like? ")
	attempts_remaining = attempts
	target = randomWord()
	blanks = '*' * len(target)
	incorrect_guesses = []


def getGuess():
	"""Request that the user enter a character
	TODO Validate the user input"""
	guess = raw_input("Please enter a single character: ")
	return guess


def makeMove():
	for x in xrange(1, attempts+1):
		g = getGuess()
		for i, char in enumerate(target):
			if g == char:
				print("OMG! That letter is in the word.")
				blanks[i] = char
				print blanks
			else:
				attempts -= 1
				print("Not in word. You have {} attempts remaining".format(attempts))


def function():
	pass

