from wordbank import randomWord
import string

lang = raw_input("Would you like English (e) or German (g)? ")
target = randomWord(lang)
blanks = ['*'] * len(target)
attempts = input("How many attempts to guess would you like? (Max 15) ")
attempts_remaining = attempts
already_guessed = []
game_over = False


def getGuess():
	"""Request that the user enter a character
	TODO Validate the user input"""
	guess = raw_input("Please enter a single character: ")
	return guess


def checkGuess(guess):
	"""Returns boolean (and index if True) """
	return [i for i, g in enumerate(target) if g == guess]


def makeMove(attempts):
	while attempts > 0:
		g = getGuess()
		while g in already_guessed:
			print("You have already guessed '{}'".format(g))
			g = getGuess()
		already_guessed.append(g)
		indexes = checkGuess(g)
		if not indexes:
			attempts -= 1
			print("Not in word. You have {} attempts remaining".format(attempts))
			print string.join(blanks, '')
		else:
			for i in indexes:
				blanks[i] = g
			print("You got one!")
			print string.join(blanks, '')


makeMove(attempts)

