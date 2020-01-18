from utils import detector_utils as detector_utils
import cv2
import datetime
import argparse
import keys

detection_graph, sess = detector_utils.load_inference_graph()

if __name__ == '__main__':

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
    args = parser.parse_args()

    # Window and variables setup
    cap = cv2.VideoCapture(args.video_source)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    start_time = datetime.datetime.now()
    num_frames = 0
    im_width, im_height = (cap.get(3), cap.get(4))

    window_name = 'Virtual Piano'

    #TODO change to fullscreen
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Init the number of keys and classes
    num_keys = 8
    keys = keys.Keys(im_width, im_height, num_keys)
    drawer = detector_utils.Drawer(keys)

    while True:
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        ret, image_np = cap.read()


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
        drawer.draw_box_on_image(args.score_thresh,
                                 scores,
                                 boxes,
                                 im_width,
                                 im_height,
                                 image_np
                                 )

        # Draw keyboard on image
        image_np = drawer.draw_keyboard(image_np, im_width, im_height)

        # Calculate Frames per second (FPS)
        num_frames += 1
        elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
        fps = num_frames / elapsed_time


        # Display FPS on frame
        if (args.fps > 0):
            detector_utils.draw_fps_on_image("FPS : " + str(int(fps)),
                                             image_np)


        # Flip the image so it's a mirron-like
        image_np = cv2.flip(image_np, 1)

        cv2.imshow('Virtual Piano',
                   cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
                   )

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
