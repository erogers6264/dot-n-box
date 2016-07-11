from wordbank import randomWord


target = randomWord()


attempts = input("How many attempts to guess would you like? ")
attempts_remaining = attempts


def getGuess():
	"""Request that the user enter a character
	TODO Validate the user input"""
	guess = raw_input("Please enter a single character: ")
	return guess


def startGame():
	pass


def makeMove():
	pass


def function():
	pass


for x in xrange(1, attempts+1):
	g = getGuess()
	for i, char in enumerate(target):
		if g == char:
			print True
		else:
			attempts -= 1
			print False