import time
from threading import Thread, Lock
import sys

lock = Lock()

def animate_text(text, duration):
    total_chars = len(text)
    delay = duration / total_chars
    with lock:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()  

def sing_lyric(lyric, delay, duration):
    time.sleep(delay) 
    animate_text(lyric, duration)

def sing_song():
    lyrics = [
        ("Kapag magulo na ang mundo", 0.0, 3.2),
        ("Ikaw ang payapang hinahanap hanap kooooo", 3.5, 6.0),
        ("Tumakbo karin patungo sakin", 14.0, 3.0),
        ("Kapag bumibigat na ang iyong dibdib", 17.0, 6.7),
        ("Ika'y sasalubongin", 25.7, 5.0),
        ("ohh, ohhhhhh", 32.2, 3.5),
    ]

    threads = []
    for lyric, delay, duration in lyrics:
        t = Thread(target=sing_lyric, args=(lyric, delay, duration))
        threads.append(t)
        t.start()

    for thread in threads: 
        thread.join()

if __name__ == "__main__":  
    sing_song()
