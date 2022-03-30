""" """

import pyaudio
import numpy as np

TWOPI = np.pi * 2

class Oscillator():
    currentPhase = 0
    increment = 0
    frequency = 440.0
    isPlaying = False
    sr = 44100
    f = lambda x : np.sin(x)

    oscillators = {
        'sine': lambda x : np.sin(x),
        'saw_up': lambda x : np.abs( (x%TWOPI) /np.pi) - 1.0,
    }

    def __init__(self, audioEngine, type = 'sine'):
        self.p = audioEngine
        self.f = self.oscillators[type]

    def start(self):
        if self.isPlaying:
            return None
        self.stream = self.p.open(format=pyaudio.paFloat32,
                            channels=1,
                            rate=self.sr,
                            output=True,
                            stream_callback = self.callback,
                            frames_per_buffer=512)
        self.isPlaying = True
        return True

    def stop(self):
        if not self.isPlaying:
            return False
        self.stream.stop_stream()
        self.stream.close()
        self.isPlaying = False
        return True
    
    def getSamples(self, frame_count):
        current_frame = self.currentPhase * self.sr / ( 2*np.pi * self.frequency )
        samples = (np.sin(TWOPI*np.arange(current_frame, current_frame + frame_count)*self.frequency/self.sr)).astype(np.float32)
        self.currentPhase =  ( TWOPI * self.frequency * (current_frame + frame_count ) / self.sr ) % TWOPI
        return samples

    def change_frequency(self, frequency):
        self.frequency = frequency
        self.increment = self.frequency * TWOPI / self.sr

    def callback(self, in_data, frame_count, time_info, status):
        current_frame = self.currentPhase * self.sr / ( 2*np.pi * self.frequency )
        samples = (self.f(TWOPI*np.arange(current_frame, current_frame + frame_count)*self.frequency/self.sr)).astype(np.float32)
        self.currentPhase =  ( TWOPI * self.frequency * (current_frame + frame_count ) / self.sr ) % TWOPI
        return (samples, pyaudio.paContinue)