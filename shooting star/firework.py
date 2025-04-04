import sys
from time import sleep
import time 

def print_colored_text(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m", end='')

def print_lyrics():
    lines = [
        ("Ikaw kasi eh..", 0.2),
        ("Close na kayo", 0.2),
        ("Nag confesss", 0.2),
        ("Ka paa...", 0.2),
    ]

    delays = [1.3, 1.7, 3.5, 1.4, 6]
    colors = [97, 97, 97, 97, 91]

    for i, ((line, char_delay), color) in enumerate(zip(lines, colors)):
        for char in line:
            print_colored_text(char, color)
            sys.stdout.flush()
            sleep(char_delay)
        time.sleep(delays[i])
        print('')

print_lyrics()