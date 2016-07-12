from wordbank import randomWord
import string

attempts = input("How many attempts to guess would you like? ")
attempts_remaining = attempts
target = randomWord()
blanks = ['*'] * len(target)
incorrect_guesses = []



def getGuess():
	"""Request that the user enter a character
	TODO Validate the user input"""
	guess = raw_input("Please enter a single character: ")
	return guess

def checkGuess(guess, target):
		for i, char in enumerate(target):
			if g == char:
				print("OMG! That letter is in the word.")
				blanks[i] = char
				print string.join(blanks, '')
			else:
				print("Not in word. You have {} attempts remaining".format(attempts))


def makeMove(attempts):
	while attempts > 0:
		g = getGuess()
		attempts -= 1

makeMove(attempts)

