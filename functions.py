import pygame

def update():
    pygame.display.update()

def transform(item, size):
    return pygame.transform.scale(item, size)


def flip_horizontal(item):
    return pygame.transform.flip(item, True, False)

def flip_vertical(item):
    return pygame.transform.flip(item, False, True)

def test_function():
    print("Hi i am a test")

def comicsans(x):
    return pygame.font.SysFont('comicsans', x)

def savegame(f, dictionary):
    with open(f, "w") as x:
        for key, value in dictionary.items():
            x.write(str(key) + " " + str(value) + "\n") ##convert to string to prevent int errors


##COLOURS##
WHITE = (255,255,255)
FOCUS = (255, 225, 73)
BLACK = (0,0,0)
DARKERGRAY = (27,27,27)
DARKGRAY = (65,60,60)
LIGHTGRAY = (166,166,166)
DARKGREEN = (9,75,15)
GREEN = (20,202,38)
DARKERBLUE = (14, 52, 117)
LIGHTBLUE = (62, 120, 222)
RED = (217, 11, 2)