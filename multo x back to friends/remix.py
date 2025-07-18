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
        ("Pasindi na ng ilaw", 4.5),
        ("Minumulto na'ko ng damdamin ko, ng damdamin ko", 6.8),
        ("How can we go back to being friends", 4.5),
        ("Dinadalaw mo 'ko bawat gabi", 2.8),
        ("Pagpapahirap sa'yo", 2.6),
        ("How can you look at me and pretend", 3.5),
        ("Haplos mo'y ramdam parin sa dilim?", 3.4),
        ("Ma mayapa?  Hindi na", 2.7),
        ("How can we go Back to being friends", 3.4),
        ("When we just shared a bed", 3.9),
    ]

    for line, duration in lyrics:
        typewriter(line, duration)

if __name__ == "__main__":
    play_song()
