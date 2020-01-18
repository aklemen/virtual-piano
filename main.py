from collections import namedtuple
import cv2
from playsound import playsound
import time
import threading
from custom_timer import CustomTimer

# TODO
# Klaviatura naj bo v spodnjem delu slike
# Na začetku roke postaviš na vrh slike za inicializacijo, potem se pokaže tipkovnica
# Popravi igranje, da se ne ponavlja nota konstantno na vsak frame
# Popravi zamik speech recognitiona


Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')

sounds = ["c1", "d1", "e1", "f1", "g1", "a1", "h1", "c2", "d2", "e2", "f2", "g2", "a2", "h2"]
sounds = ["".join(("../notes/", filename, ".wav")) for filename in sounds]
print(sounds[0])


def intersection(a, b):
    dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
    dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
    if (dx >= 0) and (dy >= 0):
        return True
    return False

st = 0
bo = False
before = False


def checkCoordinates(frame, x1, y1, x2, y2, position):
    global st
    global bo
    global before
    global timer

    temp = Rectangle(x1, y1, x2, y2)

    unit = 46

    c4 = Rectangle(0, 0, 200, 200)
    color = (220,20,60,0.3)

    cv2.rectangle(frame, (c4[0], c4[1]), (c4[2], c4[3]), color, 3)


    if intersection(temp, c4) and position == "left":
        if before == False:
            before = True
            st += 1
            print("Playing ", st)
            playsound(sounds[0], block=False)

    elif position == "left":
        before = False


