import time
import sys

def typewriter_effect(text, total_time=3.5):
    delay = total_time / len(text)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print("")

def sing_song():
    lyrics = [
        "Di mo ba ako lilisanin?",
        "Hindi pa ba sapat pagpapahirap sakin?",
        "Hindi na ba ma-mamayapa?",
        "Hindi na ba ma-mayapa?",
        "Hindi na makalaya",
        "Dinadalaw mo ko bawat gabi",
        "Wala mang nakikita",
        "Haplos mo'y ramdam parin sa dilim"
    ]
    
    for line in lyrics:
        typewriter_effect(line, total_time=3.5)
        time.sleep(0.9)

if __name__ == "__main__":
    sing_song()
