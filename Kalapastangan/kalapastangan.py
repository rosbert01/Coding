import time
import sys

print("\n\n")

lyrics = [
    "Oh, ooh",
    "Mamamatay akong nakangiti",
    "Kapag ikaw ang nasa aking tabi",
    "Mabubuhay akong nagsisisi",
    "Kapag isang araw hindi kita mapapangiti",
    "Kalapastangan ang 'di ka ibigin",
    "Kalokohan ang 'di ka isipin",
    "Kung ang mundo ay biglang gugunawin",
    "Ikaw ang una kong hahanapin",
]

line_delays = [4.6, 1.22, 1.21, 1.15, 1.13, 1.13, 1.13, 1.12, 1.12]
char_delays = [0.49, 0.13, 0.13, 0.12, 0.10, 0.10, 0.10, 0.10, 0.10]

def type_out(text, char_delay):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(char_delay)
    print()

def play_lyrics(lyrics, line_delays, char_delays):
    for i in range(len(lyrics)):
        type_out(lyrics[i], char_delays[i])
        time.sleep(line_delays[i])

if __name__ == "__main__":
    play_lyrics(lyrics, line_delays, char_delays)
