#!/usr/bin/env python3
# 💻🔀🗑️ Keep or Sweep, v0.1.0 for desktop
# Show a random file so you can clean your stuff
# Simply make executable and click (or run as python3 keeporsweep.py)
# http://keeporsweep.net

import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


FloatLayout:
    Label:
        text: "Image"
        pos_hint: {'x': .1, 'y': .4}
        size_hint: .8, .6
    Button:
        text: "Keep"
        pos_hint: {'x': .7, 'y': .1}
        size_hint: .2, .2
    Button:
        text: "Sweep"
        pos_hint: {'x': .1, 'y': .1}
        size_hint: .2, .2

class SwipeView(GridLayout):

    def __init__(self, **kwargs):
        super(SwipeView, self).__init__(**kwargs)
        self.cols = 3
        self.add_widget(Label(text='Sweep'))
        self.add_widget(Label(text='Keep'))


class KeepOrSweep(App):

    def build(self):
        return SwipeView()


if __name__ == '__main__':
    KeepOrSweep().run()
