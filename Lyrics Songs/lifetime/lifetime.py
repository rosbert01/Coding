import time
import sys

def type_line(text, delay=0.09):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


lyrics = [
    (0.4, "Oh, you were a good dream"),
    (4.4, "Smoke and ashes from these letters I'm burning"),
    (9.2, "No fairytale ending if there was no beginning"),
    (15.0, "Is it even worth it to reminisce?"),
    (19.0, "How do you grieve for a love that did not even exist"),
    (26.5, "Was there a lifetime waiting for us"),
    (30.5, "In a world when I was yours?"),
    (36.5, "Was it the wrong time? What if we tried"),
    (40.5, "Giving in a little more"),
    (44.0, "To the warmth we had before"),
]

start = time.time()

for timestamp, line in lyrics:
    while time.time() - start < timestamp:
        time.sleep(0.05)
    type_line(line)