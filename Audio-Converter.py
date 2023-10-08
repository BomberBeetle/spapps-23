import cv2
import numpy as np
import json
from scipy.io.wavfile import write
import sounddevice as sd
import time

maxfreq = 4186
minfreq = 27.5

sps = 44100
dur = 1.0
att = 0.3

objects = {}

with open("objects.json", 'r') as file:
    objects = json.loads(file.read())

for idx in objects.keys():
    imagem = cv2.imread("objects/object{}.png".format(idx))
    imagem_gray = cv2.cvtColor(imagem, cv2.COLOR_RGBA2GRAY)

    avg_value, _,_,_ = cv2.mean(imagem_gray)
    
    freq = (avg_value - 0) * (maxfreq - 255) // (255 - 0) + minfreq

    each_sample_number = np.arange(dur* sps)
    wave = np.sin(2 * np.pi * each_sample_number * freq / sps)
    wave_atten = wave*att
    
    scaled = np.int16(wave_atten/np.max(np.abs(wave_atten)) * 32767)
    write('objects/object{}.wav'.format(idx), sps, scaled)
    
