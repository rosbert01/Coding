import time


lyrics_with_delays = [
    ("Simula sa wakas na 'di matuklasan", 4.5),
    ("Pabalik kung saan 'di na natagpuan", 3.9),
    ("Ang mga matang nakatanaw sa umpisa", 3.8),
    ("Ng yugtong 'di na sana naisulat pa", 3.8),
    ("Simula sa wakas na 'di matuklasan", 3.9),
    ("Pabalik kung saan 'di na natagpuan", 4.2),
    ("Ang mga matang nakatanaw sa umpisa", 3.8),
    ("Ng yugtong 'di na sana naisulat pa", 4.0),
    ("Sa lahat ng pahinang sinulat ng tadhana'y", 4.5),
    ("Ikaw at ikaw at ikaw pa rin", 3.5),
    ("Ang yugtong paulit-ulit kong babalik-balikan", 5.0),
    ("Sigaw ay sigaw ay ikaw pa rin", 4.5),
]

def typewriter_effect(text, duration):
    print("\r", end="") 
    delay = duration / max(len(text), 1)
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()  

def display_lyrics():
    for line, duration in lyrics_with_delays:
        typewriter_effect(line, duration)
        time.sleep(0.5)  

if __name__ == "__main__":
    display_lyrics()
    print("\n=== End of Lyrics ===")