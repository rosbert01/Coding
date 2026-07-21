import time
import sys

def typewriter_effect(text, total_time=5.9):
    delay = total_time / len(text)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print("")

def sing_song():
    lyrics = [
        "Kung sakaling mapundi Ang pag-ibig mo sa akin",
        "Ay hayaan mo 'kong magbigay Ng liwanag para sa 'tin",
        "Akala ko tayo hanggang dulo Ba't ngayon nag-iisa ako?",
        "O 'di ba wala akong natutunan",
        "Ang hirap mo pa ring kalimutan"
    ]
    
    for line in lyrics:
        typewriter_effect(line, total_time=5.8)

        time.sleep(1.4) 
if __name__ == "__main__":
    sing_song()
