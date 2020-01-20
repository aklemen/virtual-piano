from utils import detector_utils as detector_utils
import cv2
import datetime
import argparse
from keys import Keys
import speech_recognition as sr

detection_graph, sess = detector_utils.load_inference_graph()

class Detector:
    def __init__(self):
        # Argument for 'customization'
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-sth',
            '--scorethreshold',
            dest='score_thresh',
            type=float,
            default=0.2,
            help='Score threshold for displaying bounding boxes')
        parser.add_argument(
            '-fps',
            '--fps',
            dest='fps',
            type=int,
            default=0,
            help='Show FPS on detection/display visualization')
        parser.add_argument(
            '-src',
            '--source',
            dest='video_source',
            default=0,
            help='Device index of the camera.')
        parser.add_argument(
            '-wd',
            '--width',
            dest='width',
            type=int,
            default=320,
            help='Width of the frames in the video stream.')
        parser.add_argument(
            '-ht',
            '--height',
            dest='height',
            type=int,
            default=180,
            help='Height of the frames in the video stream.')
        self.args = parser.parse_args()

        # Window and variables setup
        self.cap = cv2.VideoCapture(self.args.video_source)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.args.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.args.height)

        self.start_time = datetime.datetime.now()
        self.num_frames = 0
        self.im_width, self.im_height = (self.cap.get(3), self.cap.get(4))

        window_name = 'Virtual Piano'

        #TODO change to fullscreen
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        # cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        # Init the number of keys and classes
        num_keys = 7
        box_size = 10
        self.keys = Keys(self.im_width, self.im_height, num_keys, box_size)
        self.drawer = detector_utils.Drawer(self.keys)


    def run(self):
        # To center text
        font = cv2.FONT_HERSHEY_COMPLEX
        text = "Postavite roki v polja."
        textsize = cv2.getTextSize(text, font, 1, 2)[0]
        textX = (self.im_width - textsize[0]) / 2
        textY = (self.im_height + textsize[1]) / 2


        while True:
            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            ret, image_np = self.cap.read()

            try:
                image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
            except:
                print("Error converting to RGB")

            # Detection.
            # 'boxes' contains the bounding box cordinates for hands detected
            # 'scores' contains the confidence for each of the boxes

            boxes, scores = detector_utils.detect_objects(image_np,
                                                          detection_graph,
                                                          sess
                                                          )

            # Draw bounding boxes on frame
            self.drawer.draw_box_on_image(self.args.score_thresh,
                                     scores,
                                     boxes,
                                     self.im_width,
                                     self.im_height,
                                     image_np
                                     )

            # Draw keyboard on image
            image_np = self.drawer.draw_keyboard(image_np, self.im_width, self.im_height)

            # Calculate Frames per second (FPS)
            self.num_frames += 1
            elapsed_time = (datetime.datetime.now() - self.start_time).total_seconds()
            fps = self.num_frames / elapsed_time


            # Display FPS on frame
            if self.args.fps > 0:
                detector_utils.draw_fps_on_image("FPS : " + str(int(fps)),
                                                 image_np)


            # Flip the image so it's a mirror-like
            image_np = cv2.flip(image_np, 1)

            cv2.putText(image_np, text, (int(textX), int(textY)), font, 1, (2, 105, 164), 2)

            cv2.imshow('Virtual Piano',
                       cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
                       )

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    def speech_recognition(self):
        print("Listening...")
        recognizer = sr.Recognizer()
        recognizer.listen_in_background(sr.Microphone(), self.callback)

    def callback(self, recognizer, audio):
        try:
            speech = recognizer.recognize_google(audio, language="sl-SI")
            print("You said: " + speech)

            # Change instruments
            if (("zamenjaj" in speech) or ("spremeni" in speech)) and ("zvok" in speech):
                self.keys.change_sound("change")
            elif "klavir" in speech:
                self.keys.change_sound("piano")
            elif "orgl" in speech:
                self.keys.change_sound("organ")
            elif ("piščal" in speech) or ("flavt" in speech):
                self.keys.change_sound("flute")

            # Change colors
            if (("zamenjaj" in speech) or ("spremeni" in speech)) and ("barv" in speech):
                self.drawer.change_color("change")
            if "črn" in speech:
                self.drawer.change_color("black")
            elif "modr" in speech:
                self.drawer.change_color("blue")
            elif "rdeč" in speech:
                self.drawer.change_color("red")
            elif "zelen" in speech:
                self.drawer.change_color("green")


        except sr.UnknownValueError:
            print("I didn't understand.")
        except sr.RequestError as e:
            print("Google Speech Recognition not available {0}".format(e))


if __name__ == '__main__':
    detector = Detector()
    detector.speech_recognition()
    detector.run()
