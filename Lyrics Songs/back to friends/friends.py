import time
import sys

def typewriter(text, duration):
    if not text.strip():  
        time.sleep(duration)
        print()  
        return

    delay = duration / len(text)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def play_song():
    lyrics = [
        ("I was scared to take a breath", 2.9),
        ("Didn't want you to move your head", 3.0),
        ("How can we go back to being friends", 2.7),
        ("When we just shared a bed? (Yeah)", 4.2),
        ("How can you look at me and pretend", 4.6),
        ("I'm someone you've never met?", 3.9)
    ]

    for line, delay in lyrics:
        typewriter(line, delay)
        time.sleep(0.8)

play_song()
