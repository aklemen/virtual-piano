# Setup instructions

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

When everything is installed, we can run the program using:

```
python main.py
```

The results are best if we have good lighting and plain background, but it should work good even if the latter requirement is not satisfied.

# In use

|
:-------------------------:|:-------------------------:
![](https://user-images.githubusercontent.com/56405660/75018019-80ba3e80-548e-11ea-807a-8febea18df7d.jpg)  |  ![](https://user-images.githubusercontent.com/56405660/75018046-8e6fc400-548e-11ea-8452-ddad3e3d778b.jpg)

## Voice commands

When the application is running, you can change sound or interface color using voice commands. You will need a microphone for this.

* COLOR: *"change color"*, *"switch color"*, *"red"*, *"blue"*, *"green"*
* SOUND: *"change sound"*, *"switch sound"*, *"piano"*, *"organ"*, *"flute"*

If the command is successful, you will hear a sound effect.
