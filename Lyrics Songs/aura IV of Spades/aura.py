import os
import time
import sys


lyrics = [
    ("Nasa'n ka na?", 2.5),
    ("Tingnan natin nang husto", 1.5),
    ("(Pagmasdan mo nang maigi)", 1.8),
    ("Ang makulay kong mundo", 2.2),
    ("(Mga tao sa paligid)", 2.0),
    ("Kahit minsa'y magulo", 1.7),
    ("(Kahit medyo alanganin)", 1.8),
    ("Yayakapin nang buo", 2.0),
    ("(Ikaw pa rin ang hahanapin)", 3.0)
]


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def typewriter(text, speed=0.10):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()


for line, delay in lyrics:
    clear_screen()
    typewriter(line, speed=0.10)  
    time.sleep(delay) 
