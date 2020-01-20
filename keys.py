from collections import namedtuple
import cv2
from playsound import playsound
import time
import threading
from custom_timer import CustomTimer

# TODO
# Na začetku roke postaviš na vrh slike za inicializacijo, potem se pokaže tipkovnica


def intersection(a, b):
    dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
    dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
    if (dx >= 0) and (dy >= 0):
        return True
    return False


class Keys:

    def __init__(self, im_width, im_height, num_keys, box_size, unit_w, unit_h):
        # Named tuple for easier work with rectangle coordinates
        self.Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')

        # Storing width and height of image just in case
        self.im_width = im_width
        self.im_height = im_height

        # Lists of sound files
        self.sounds = []
        self.notes = ["c1", "d1", "e1", "f1", "g1", "a1", "h1", "c2", "d2", "e2", "f2", "g2", "a2", "h2"]
        self.notes = self.notes[::-1]

        self.sounds.append(["".join(("sounds/", filename, ".wav")) for filename in self.notes])
        self.sounds.append(["".join(("sounds/organ_", filename, ".wav")) for filename in self.notes])
        self.sounds.append(["".join(("sounds/flute_", filename, ".wav")) for filename in self.notes])

        self.current_sound = 0

        # Initializing the list of keys with their coordinates
        self.num_keys = num_keys
        self.list_keys = []

        # For checking intersection
        self.previous_key_left = -1
        self.previous_key_right = -1
        self.box_size = box_size
        self.outside_keys = self.Rectangle(0, 0, im_width, int(im_height - unit_h) - (box_size*2))

        for i in range(num_keys):
            temp_rect = self.Rectangle(int(unit_w*i), int(im_height - unit_h), int(unit_w*(i+1)), int(im_height))
            self.list_keys.append(temp_rect)

    def change_sound(self, instrument):
        if instrument == "change":
            if self.current_sound < len(self.sounds) - 1:
                self.current_sound += 1
            else:
                self.current_sound = 0
            playsound("sounds/success.mp3")
        elif instrument == "piano":
            self.current_sound = 0
            playsound("sounds/success.mp3")
        elif instrument == "organ":
            self.current_sound = 1
            playsound("sounds/success.mp3")
        elif instrument == "flute":
            self.current_sound = 2
            playsound("sounds/success.mp3")

    def check_coordinates(self, frame, x1, y1, x2, y2, position):

        temp_rect = self.Rectangle(x1, y1, x2, y2)

        if intersection(temp_rect, self.outside_keys):
            if position == "left":
                self.previous_key_left = -1
            elif position == "right":
                self.previous_key_right = -1
        else:
            for i in range(len(self.list_keys)):
                key = self.list_keys[i]
                if intersection(temp_rect, self.list_keys[i]):
                    if position == "left" and self.previous_key_left != i:
                        playsound(self.sounds[self.current_sound][i], block=False)
                        cv2.rectangle(frame, (key[0], key[1]), (key[2], key[3]), (132, 123, 123), -1)
                        self.previous_key_left = i
                    elif position == "right" and self.previous_key_right != i:
                        playsound(self.sounds[self.current_sound][i], block=False)
                        cv2.rectangle(frame, (key[0], key[1]), (key[2], key[3]), (132, 123, 123), -1)
                        self.previous_key_right = i
                    break
