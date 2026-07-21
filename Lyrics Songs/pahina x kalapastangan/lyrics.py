import time
import sys

def animate_lyrics():
   
    lyrics = [
        ("Simula sa wakas na 'di matuklasan", 4.3),
        ("Pabalik kung saan 'di na natagpuan", 3.9),
        ("Ang mga matang nakatanaw sa umpisa", 3.9),
        ("Ng yugtong 'di na sana naisulat pa", 4.5),
        ("Mamamatay akong nakangiti", 4.9),
        ("Kapag ikaw ang nasa aking tabi", 4.0),
        ("Mabubuhay akong nagsisisi", 4.5),
        ("Kapag isang araw hindi kita mapapangiti", 4.0),
        ("Kalapastangan ang 'di ka ibigin", 4.2),
        ("Kalokohan ang 'di ka isipin", 3.9),
        ("Kung ang mundo ay biglang gugunawin", 4.0),
        ("Ikaw ang una kong hahanapin", 4.3),
    ]
    time.sleep(1)  

    for line, duration in lyrics:
       
        typing_duration = duration * 0.70
        pause_duration = duration * 0.30
        
      
        char_delay = typing_duration / len(line)

        for char in line:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(char_delay)

        
        print() 
        time.sleep(pause_duration)

if __name__ == "__main__":
    animate_lyrics()