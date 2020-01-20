
import speech_recognition as sr
def callback(recognizer, audio):                          # this is called from the background thread
    try:
        print("You said " + recognizer.recognize_google(audio))  # received audio data, now need to recognize it
    except:
        print("Oops! Didn't catch that")
r = sr.Recognizer()
r.listen_in_background(sr.Microphone(), callback)

import time
while True: time.sleep(0.1)
