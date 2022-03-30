""" """

import pyaudio
import numpy as np
from timeit import default_timer as timer
from streamoscillator import Oscillator

SAMPLE_RATE = 44100
TWOPI = np.pi * 2
TWOPIOVERSR = np.pi * 2 / SAMPLE_RATE

class OscillatorStream():
    currentPhase = 0
    increment = 0
    frequency = 440.0
    isPlaying = False
    sr = SAMPLE_RATE
    oscillators = {}

    def __init__(self, audioEngine):
        self.p = audioEngine

    def audio_callback(self, in_data, frame_count, time_info, status):
        samples = np.zeros(frame_count, np.float32)
        oscillators = self.oscillators.copy()
        for key, value in oscillators.items():

            start_time = timer()

            frequency = value.frequency
            
            samples += value.getSamples(frame_count)
            

            end_time = timer()
            print(end_time-start_time)

        if len(oscillators) > 0:
            samples /= len(oscillators)

        return ( samples, pyaudio.paContinue )

    def start(self):
        if self.isPlaying:
            return None
        self.stream = self.p.open(format=pyaudio.paFloat32,
                            channels=1,
                            rate=self.sr,
                            output=True,
                            stream_callback = self.audio_callback,
                            frames_per_buffer=1024)
        self.isPlaying = True
        return True

    def stop(self):
        if not self.isPlaying:
            return False
        self.stream.stop_stream()
        self.stream.close()
        self.isPlaying = False
        return 

    def addOscillator(self, id, frequency, type):
        osc = Oscillator(self.p)
        self.oscillators[str(id)] = osc 
   

    def removeOscillator(self, id):
        del self.oscillators[str(id)]

    def changeFrequency(self, id, frequency):
        self.oscillators[str(id)].frequency = frequency

     
        





















