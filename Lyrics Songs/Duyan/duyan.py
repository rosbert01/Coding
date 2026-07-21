import time
import sys



char_delay = 0.07  
line_pause_default = 1.5  

lyrics = [
    ("Kakampi kita,", 1.9),
    ("'di ka mag-iisa", 1.4),
    ("Mainit man o malamig", 1.9),
    ("ang ating kabanata", 1.8),

    ("", 1.2),

    ("Yayakapin ko", 1.5),
    ("ang iyong init", 1.4),
    ("At sasamahan kita", 1.9),
    ("hanggang sa bulan", 1.9),
    ("Sisikapin kong", 1.8),
    ("maging kanlungan mo", 1.7),
    ("At sabay nating punuin", 3.9),
    ("Ng alaala", 2.2),
    ("ang ating duyan", 4.0),
]

def type_line(text, delay):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(char_delay)
    print()
    time.sleep(delay)


def karaoke_play():
    
    time.sleep(1)

    for line, pause in lyrics:
        type_line(line, pause if pause else line_pause_default)

   




if __name__ == "__main__":
    karaoke_play()
