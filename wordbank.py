# 
# Module should return a list, words, from which a random selection is chosen for
# use in a game of hangman. Will possibly expand to retrieve a list of words of a
# user chosen category. Or something dynamic of that nature.
#

import random


german_words = ["sein", "haben", "werden", "koennen", "muessen", "sagen", "machen",
"geben", "kommen", "sollen", "wollen", "gehen", "wissen", "sehen", "lassen",
"stehen", "finden", "bleiben", "liegen", "heissen", "denken", "nehmen", "tun",
"duerfen", "glauben", "halten", "nennen", "moegen", "zeigen", "fuehren",
"sprechen,", "bringen", "leben", "fahren", "meinen", "fragen", "kennen",
"gelten", "stellen", "spielen", "arbeiten", "brauchen", "folgen", "lernen",
"bestehen", "verstehen", "setzen", "bekommen", "beginnen", "erzaehlen",
"versuchen", "schreiben", "laufen", "erklaeren", "entsprechen", "sitzen",
"ziehen", "scheinen", "fallen", "gehoeren", "entstehen", "erhalten", "treffen",
"suchen", "legen", "vorstellen", "handeln", "erreichen", "tragen", "schaffen",
"lesen", "verlieren", "darstellen", "erkennen", "entwickeln", "reden",
"aussehen", "erscheinen", "bilden", "anfangen", "erwarten", "wohnen",
"betreffen", "warten", "vergehen", "helfen", "gewinnen", "schliessen", "fuehlen",
"bieten", "interessieren", "erinnern", "ergeben", "anbieten", "studieren",
"verbinden", "ansehen", "fehlen", "bedeuten", "vergleichen"]

english_words = ["acres", "adult", "advice", "arrangement", "attempt", "august", "autumn",
"border", "breeze", "brick", "calm", "canal", "casey", "cast", "chose", "claws",
"coach", "constantly", "contrast", "cookies", "customs", "damage", "danny",
"deeply", "depth", "discussion", "doll", "donkey", "egypt", "ellen",
"essential", "exchange", "exist", "explanation", "facing", "film", "finest",
"fireplace", "floating", "folks", "fort", "garage", "grabbed", "grandmother",
"habit", "happily", "harry", "heading", "hunter", "illinois", "image",
"independent", "instant", "january", "kids", "label", "lee", "lungs",
"manufacturing", "martin", "mathematics", "melted", "memory", "mill", "mission",
"monkey", "mount", "mysterious", "neighborhood", "norway", "nuts",
"occasionally", "official", "ourselves", "palace", "pennsylvania",
"philadelphia", "plates", "poetry", "policeman", "positive", "possibly",
"practical", "pride", "promised", "recall", "relationship", "remarkable",
"require", "rhyme", "rocky", "rubbed", "rush", "sale", "satellites",
"satisfied", "scared", "selection", "shake", "shaking", "shallow", "shout",
"silly", "simplest", "slight", "slip", "slope", "soap", "solar", "species",
"spin", "stiff", "swung", "tales", "thumb", "tobacco", "toy", "trap", "treated",
"tune", "university", "vapor", "vessels", "wealth", "wolf", "zoo"]

def randomWord(lang):
	if lang.lower() == 'e':
		print("English chosen")
		rw = random.choice(english_words)
	else:
		print("German chosen")
		rw = random.choice(german_words)
	return rw
