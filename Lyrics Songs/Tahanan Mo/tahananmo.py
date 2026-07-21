import sys
from time import sleep

def print_lyrics():
    lines = [
        ("Ipaglalaban ko ohhh", 0.24),
        ("Tahanan mo ako, di magbabago yon", 0.26),
        ("At pag ika'y nawawala, tingin ka lang sa 'king mata", 0.13),
        ("Pagmamahal sa'yo di mauubos yon", 0.22),
        ("Lalabanan ko lahat para sa'yo", 0.20),
        ("Basta't nandito lang ako sa tabi mo", 0.18)
    ]

    for line, delay in lines:
        for char in line:
            sys.stdout.write(char)
            sys.stdout.flush()
            sleep(delay)
        print()  

print_lyrics()
