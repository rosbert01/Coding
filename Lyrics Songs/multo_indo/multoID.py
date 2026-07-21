import time
import sys

def typewriter_effect(text, total_time=2.0):
    delay = total_time / len(text)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print("")

def sing_song():
    lyrics = [
        "Dihantui oleh bayang-bayang mu",
        "Bayang-bayang mu",
        "Tinggalkan lah ku sendiri",
        "Suda cukup, ku tak mampu menahan sakit",
        "Akan kah ku bisa tinggalkannya?",
        "Akan kah ku bisa lupakan dirinya?",
        "Terperangkap olehnya",
        "Tiap malam datang menghampi"
    ]
    
    for line in lyrics:
        typewriter_effect(line, total_time=2.0)
        time.sleep(1.7)

if __name__ == "__main__":
    sing_song()
