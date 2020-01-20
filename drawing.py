from playsound import playsound
import cv2

class Drawer:
    def __init__(self, keys, unit_w, unit_h):
        self.p1 = [(0, 0), (0, 0)]
        self.p2 = [(0, 0), (0, 0)]
        self.p_center = [(0, 0), (0, 0)]

        # Number of hands to detect. Don't change this.
        self.num_hands_detect = 2

        self.box_size = keys.box_size
        self.keys = keys
        self.num_keys = keys.num_keys
        self.unit_w = unit_w
        self.unit_h = unit_h

        self.colors = [(0, 0, 0, 0.3), (2, 105, 164, 0.3), (139, 0, 0, 0.3), (0, 128, 0, 0.3)]
        self.current_color = 0


    def change_color(self, color):
        if color == "change":
            if self.current_color < len(self.colors) - 1:
                self.current_color += 1
            else:
                self.current_color = 0
            playsound("sounds/success.mp3")
        elif color == "black":
            self.current_color = 0
            playsound("sounds/success.mp3")
        elif color == "blue":
            self.current_color = 1
            playsound("sounds/success.mp3")
        elif color == "red":
            self.current_color = 2
            playsound("sounds/success.mp3")
        elif color == "green":
            self.current_color = 3
            playsound("sounds/success.mp3")


    def draw_keyboard(self, frame, im_width, im_height):
        overlay = frame.copy()
        alpha = 0.4
        image_with_keys = None

        for i in range(self.num_keys):
            if i % 2 == 0:
                color = self.colors[self.current_color]
            else:
                color = (255, 255, 255, 0.3)
            t1 = (int(self.unit_w*i), int(im_height-self.unit_h))
            t2 = (int(self.unit_w*(i+1)), int(im_height))

            cv2.rectangle(frame, t1, t2, color, cv2.FILLED)
            image_with_keys = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

        return image_with_keys


    def draw_box_on_image(self, score_thresh, scores, boxes, im_width, im_height, image_np):

        position = "hands_not_present"  # This doesn't or shouldn't happen
        for i in range(self.num_hands_detect):

            if scores[0] > score_thresh and scores[1] > score_thresh:

                (left, right, top, bottom) = (boxes[i][1] * im_width, boxes[i][3] * im_width,
                                              boxes[i][0] * im_height, boxes[i][2] * im_height)

                self.p_center[i] = (int(left + (right-left)/2), int(top + (bottom-top)/2))

                # self.p1[i] = (int(left), int(top))
                # self.p2[i] = (int(right), int(bottom))

                # Rectangle coordinates
                self.p1[i] = (self.p_center[i][0]-self.box_size, self.p_center[i][1]-self.box_size)
                self.p2[i] = (self.p_center[i][0]+self.box_size, self.p_center[i][1]+self.box_size)

            # Checking coordinates to activate sounds
            # Directions are swapped, because image is flipped
            if self.p1[0][0] < self.p1[1][0]:
                if i == 0:
                    position = "right"
                elif i == 1:
                    position = "left"
            elif self.p1[0][0] > self.p1[1][0]:
                if i == 0:
                    position = "left"
                elif i == 1:
                    position = "right"

            # Draw the bounding box and text
            # cv2.rectangle(image_np, self.p1[i], self.p2[i], (77, 255, 9), 3, 1)
            # cv2.putText(image_np, position, self.p_center[i], cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

            if position != "hands_not_present":
                self.keys.check_coordinates(image_np, self.p1[i][0], self.p1[i][1], self.p2[i][0], self.p2[i][1], position)
