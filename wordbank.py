"""wordbank.py - File for holding target words and choosing one at random."""

import random


def randomWord():
    words = ["alligator", "ant", "bear", "bee", "bird", "camel", "cat",
             "cheetah", "chicken", "chimpanzee", "cow", "crocodile", "deer",
             "dog", "dolphin", "duck", "eagle", "elephant", "fish", "fly",
             "fox", "frog", "giraffe", "goat", "goldfish", "hamster",
             "hippopotamus", "horse", "kangaroo", "kitten", "lion", "lobster",
             "monkey", "octopus", "owl", "panda", "pig", "puppy", "rabbit",
             "rat", "scorpion", "seal", "shark", "sheep", "snail", "snake",
             "spider", "squirrel", "tiger", "turtle", "wolf", "zebra"]
    rw = random.choice(words)
    return rw
