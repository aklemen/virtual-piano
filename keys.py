from collections import namedtuple
import cv2
from playsound import playsound
import time
import threading
from custom_timer import CustomTimer

# TODO
# Na začetku roke postaviš na vrh slike za inicializacijo, potem se pokaže tipkovnica
# Popravi igranje, da se ne ponavlja nota konstantno na vsak frame
# Popravi zamik speech recognitiona


def intersection(a, b):
    dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
    dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
    if (dx >= 0) and (dy >= 0):
        return True
    return False


class Keys:

    def __init__(self, im_width, im_height, num_keys, box_size):
        # Named tuple for easier work with rectangle coordinates
        self.Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')

        # Storing width and height of image just in case
        self.im_width = im_width
        self.im_height = im_height

        # List of sound files
        self.sounds = ["c1", "d1", "e1", "f1", "g1", "a1", "h1", "c2", "d2", "e2", "f2", "g2", "a2", "h2"]
        self.sounds = self.sounds[::-1]
        self.sounds = ["".join(("../notes/", filename, ".wav")) for filename in self.sounds]

        # Initializing the list of keys with their coordinates
        self.num_keys = num_keys
        self.list_keys = []
        unit_w = im_width/num_keys
        unit_h = im_height/2

        # For checking intersection
        self.previous_key_left = -1
        self.previous_key_right = -1
        self.box_size = box_size
        self.outside_keys = self.Rectangle(0, 0, im_width, unit_h-(box_size*2))

        for i in range(num_keys):
            temp_rect = self.Rectangle(int(unit_w*i), int(unit_h), int(unit_w*(i+1)), int(im_height))
            self.list_keys.append(temp_rect)

    def check_coordinates(self, frame, x1, y1, x2, y2, position):
        temp_rect = self.Rectangle(x1, y1, x2, y2)

        for i in range(len(self.list_keys)):
            key = self.list_keys[i]
            if intersection(temp_rect, self.list_keys[i]):
                if position == "left" and self.previous_key_left != i:
                    playsound(self.sounds[i], block=False)
                    cv2.rectangle(frame, (key[0], key[1]), (key[2], key[3]), (132, 123, 123), -1)
                    self.previous_key_left = i
                elif position == "right" and self.previous_key_right != i:
                    playsound(self.sounds[i], block=False)
                    cv2.rectangle(frame, (key[0], key[1]), (key[2], key[3]), (132, 123, 123), -1)
                    self.previous_key_right = i
            elif intersection(temp_rect, self.outside_keys):
                if position == "left":
                    self.previous_key_left = -1
                elif position == "right":
                    self.previous_key_right = -1




"""
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
"""

