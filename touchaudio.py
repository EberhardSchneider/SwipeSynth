from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty

import numpy as np
import pyaudio
import stream

SCALE_FACTOR = .02
BASE_FREQ = 220
SEMITONERATIO = 1.0594630943592952645

class TouchAudio(Widget):

    p = None
    n_osc = 1
    stream = None
    label_output = StringProperty("H")

    def __init__(self):
        super(TouchAudio, self).__init__()
        self.p = pyaudio.PyAudio()
        self.stream = stream.OscillatorStream( self.p )
        self.stream.start()

    def on_touch_down(self, touch):
        self.stream.addOscillator(touch.uid, self.calcFrequency(touch.x), 'sine')

    def on_touch_move(self, touch):
        self.stream.changeFrequency(touch.uid,  self.calcFrequency(touch.x))
        self.label_output = str(int(self.calcFrequency(touch.x)))

    def on_touch_up(self, touch):
        self.stream.removeOscillator(touch.uid)

    def calcFrequency(self,  x):
        x = x * SCALE_FACTOR
        freq = BASE_FREQ * SEMITONERATIO**x
        return freq

class SimpleScore(Widget):
    notes = []

class TouchAudioApp(App):
    def build(self):
        return TouchAudio()

if __name__ == '__main__':
    TouchAudioApp().run()