# Utilities for object detector.

import numpy as np
import sys
import tensorflow as tf
import os
from threading import Thread, Timer
from datetime import datetime
import cv2
from utils import label_map_util
from collections import defaultdict

import keys
from custom_timer import CustomTimer


detection_graph = tf.Graph()
sys.path.append("..")

# score threshold for showing bounding boxes.
_score_thresh = 0.27

MODEL_NAME = 'hand_inference_graph'
# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join(MODEL_NAME, 'hand_label_map.pbtxt')

NUM_CLASSES = 1
# load label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(
    label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


# Load a frozen infrerence graph into memory
def load_inference_graph():

    # load frozen tensorflow model into memory
    print("> ====== loading HAND frozen graph into memory")
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        sess = tf.Session(graph=detection_graph)
    print(">  ====== Hand Inference graph loaded.")
    return detection_graph, sess

class Drawer:
    def __init__(self, keys):
        self.p1 = [(0, 0), (0, 0)]
        self.p2 = [(0, 0), (0, 0)]
        self.p_center = [(0, 0), (0, 0)]

        # Number of hands to detect. Don't change this.
        self.num_hands_detect = 2

        self.box_size = keys.box_size
        self.keys = keys
        self.num_keys = keys.num_keys

        # # Testing
        # self.previous_center_left = (100, 100)
        # self.previous_center_right = (keys.im_width-100, 100)


    def none_func(self):
        return

    def draw_keyboard(self, frame, im_width, im_height):
        unit_w = im_width/self.num_keys
        unit_h = im_height/2

        overlay = frame.copy()
        alpha = 0.4
        image_with_keys = None

        for i in range(self.num_keys):
            if i % 2 == 0:
                color = (0, 0, 0, 0.3)
            else:
                color = (255, 255, 255, 0.3)
            t1 = (int(unit_w*i), int(unit_h))
            t2 = (int(unit_w*(i+1)), int(im_height))

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
            cv2.rectangle(image_np, self.p1[i], self.p2[i], (77, 255, 9), 3, 1)
            # cv2.putText(image_np, position, self.p_center[i], cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

            # distance = 150
            #
            # if position == "left":
            #     if abs(self.previous_center_left[0] - self.p_center[i][0]) > distance or abs(self.previous_center_left[1] - self.p_center[i][1]) > distance:
            #         t1 = (self.previous_center_left[0]-self.box_size, self.previous_center_left[1]-self.box_size)
            #         t2 = (self.previous_center_left[0]+self.box_size, self.previous_center_left[1]+self.box_size)
            #         self.keys.check_coordinates(image_np, t1[0], t1[1], t2[0], t2[1], position)
            #     else:
            #         self.keys.check_coordinates(image_np, self.p1[i][0], self.p1[i][1], self.p2[i][0], self.p2[i][1], position)
            #         self.previous_center_left = self.p_center[i]
            # elif position == "right":
            #     if abs(self.previous_center_right[0] - self.p_center[i][0]) > distance or abs(self.previous_center_right[1] - self.p_center[i][1]) > distance:
            #         t1 = (self.previous_center_right[0]-self.box_size, self.previous_center_right[1]-self.box_size)
            #         t2 = (self.previous_center_right[0]+self.box_size, self.previous_center_right[1]+self.box_size)
            #         self.keys.check_coordinates(image_np, t1[0], t1[1], t2[0], t2[1], position)
            #     else:
            #         self.keys.check_coordinates(image_np, self.p1[i][0], self.p1[i][1], self.p2[i][0], self.p2[i][1], position)
            #         self.previous_center_right = self.p_center[i]


            if position != "hands_not_present":
                self.keys.check_coordinates(image_np, self.p1[i][0], self.p1[i][1], self.p2[i][0], self.p2[i][1], position)



# Show fps value on image.
def draw_fps_on_image(fps, image_np):
    cv2.putText(image_np, fps, (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (77, 255, 9), 2)


# Actual detection .. generate scores and bounding boxes given an image
def detect_objects(image_np, detection_graph, sess):
    # Definite input and output Tensors for detection_graph
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    # Each box represents a part of the image where a particular object was detected.
    detection_boxes = detection_graph.get_tensor_by_name(
        'detection_boxes:0')
    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name(
        'detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name(
        'detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name(
        'num_detections:0')

    image_np_expanded = np.expand_dims(image_np, axis=0)

    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores,
            detection_classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})
    return np.squeeze(boxes), np.squeeze(scores)


# Code to thread reading camera input.
# Source : Adrian Rosebrock
# https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/
class WebcamVideoStream:
    def __init__(self, src, width, height):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def size(self):
        # return size of the capture device
        return self.stream.get(3), self.stream.get(4)

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
