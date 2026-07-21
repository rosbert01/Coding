import time
import sys

def typewriter_effect(text, total_time=5.5):
    delay = total_time / len(text)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print("")

def sing_song():
    lyrics = [
        "Nagsimula sa simple na pasulyap-sulyap, nagpapapansin sa 'yo",
        "Umabot sa palitan ng mga mensahe, kilig na kilig ako",
        "Kumusta? Kain na, hello, magandang umaga",
        "Ingat ka, pahinga, huwag kang masyadong magpupuyat pa"
    ]
    
    for line in lyrics:
        typewriter_effect(line, total_time=5.5)
        time.sleep(1.2)

if __name__ == "__main__":
    sing_song()
