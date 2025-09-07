import time
import sys

lyrics = [
    ("'Di sasayangin ang oras at pag-ibig mo", 4.8),
    ("Mas pipiliin ko", 2.7),
    ("Ibigay lahat pati itong aking mundo", 5.1),
    ("....", 3.5),  
    ("Halika't sumayaw sa ilalim ng bituin", 5.5),
    ("Habang ako’y nakatingin sa'yo", 4.9),
    ("Wala na 'kong ibang mahihiling", 4.7),
    ("Saksi ang langit sa'tin", 5.7),
    ("", 2.5),
    ("Oh-oh, oh-oh-oh.", 3.6)
]

def typewriter(text, delay):
    if not text.strip():
        time.sleep(delay)
        return
    char_delay = delay / len(text)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(char_delay)
    print()  

print("\n🎶'Saksi ang Langit' (December Avenue)...\n")
for line, delay in lyrics:
    typewriter(line, delay)
print("\n🎵🎵")

