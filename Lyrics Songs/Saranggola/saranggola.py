import time
import sys

def typewriter_effect(text, total_time):
    delay = total_time / max(len(text), 1)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


lyrics_with_timing = [
    ("Saranggola'y lilipad sa kahel na kalangitan,", 4.2),
    ("Paalam na nga ba sa ating nakaraan?", 4.5),
    ("Ngunit sa'n man tayo hipan ng amihan,", 4.3),
    ("Di ipagpapalit ang pagkakaibigan.", 5.0)
]

for line, duration in lyrics_with_timing:
    typewriter_effect(line, duration)
    time.sleep(0.6) 
