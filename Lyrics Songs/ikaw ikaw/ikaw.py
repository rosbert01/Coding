import time
import sys

def typewriter(text, duration):
    delay = duration / max(len(text), 1)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def play_stanza():
    stanza = [
        ("Masisisi pa ba natin ang tadhana?", 3.8),
        ("Kung masaya naman ang mga alaala", 3.0),
        ("Kung bibigyan ako ng tatlong kahilingan", 4.0),
        ("Ikaw, ikaw, ikaw", 2.5),
        ("Sa paggising at pagmulat sa umaga", 2.1),
        ("Ikaw lamang ang tinatanging nakikita", 2.1),
        ("Ngunit 'pag hinahanap-hanap ay nawawala", 3.5),
        ("Wala, wala, wala sa'king tabi", 4.0),
    ]

    for line, duration in stanza:
        typewriter(line, duration)
        time.sleep(0.1)

if __name__ == "__main__":
    play_stanza()
