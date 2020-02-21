# Virtual piano

This is a virtual "air" piano application using hand tracking and speech recognition. It was made using multiple Python libraries, including HandTrack, Tensorflow, playsound, OpenCV and SpeechRecognition.

## Setup instructions

Hardware requirements:
* NVIDIA GPU with CUDA support
* Webcam
* Microphone

Software requirements:
* Python 3.7
* CUDA Toolkit 10.0
* cuDNN library for CUDA Toolkit 10.0

Python modules required:
* pip install tensorflow-gpu==1.14
* pip install opencv-python
* pip install playsound
* pip install SpeechRecognition
* pip install pyaudio

The user should have a webcam and the computer screen before him, so he can see the virtual keyboard on the screen and play it using only his hands. Also place the microphone near the user, so the system will recognize his voice commands.

When everything is ready, we can run the program using:

```
python main.py
```

The results are best if we have good lighting and plain background, but it should work good even if the latter requirement is not satisfied.

### Voice commands

When the application is running, you can change the keyboard sound or the color of interface using voice commands. You will need a microphone for this.

* COLOR: *"change color"*, *"switch color"*, *"red"*, *"blue"*, *"green"*
* SOUND: *"change sound"*, *"switch sound"*, *"piano"*, *"organ"*, *"flute"*

If the command is successful, you will hear a sound effect.

## In use

![](https://user-images.githubusercontent.com/56405660/75018019-80ba3e80-548e-11ea-807a-8febea18df7d.jpg) | ![](https://user-images.githubusercontent.com/56405660/75018046-8e6fc400-548e-11ea-8452-ddad3e3d778b.jpg)
:-------------------------:|:-------------------------:

## Acknowlegments

A big part of this project was quick and robust hand detection and tracking. I used an awesome [HandTrack](https://github.com/victordibia/handtracking) library by [victordibia](https://github.com/victordibia). Thank you!
