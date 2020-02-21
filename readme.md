# Setup instructions

Hardware requirements:
* Grafična kartica NVIDIA s podporo CUDA
* Spletna kamera
* Mikrofon

Software requirements:
* Python 3.7
* CUDA Toolkit 10.0
* cuDNN knjižnjica za CUDA Toolkit 10.0

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
