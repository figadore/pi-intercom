'''
Single button controls call functionality. Short press opens
all-way communications for hands-free mode. Next press closes the line.
Alternatively, long-pressing the button enables push-to-talk mode,
closing the line when the button is released
'''
import os
import time
import threading

import calls
from gpiozero import LED, Button

led = LED(4)
callButton = Button(26)
resetButton = Button(17)

class ButtonHandler(threading.Thread):
    '''
    Adapted from https://raspberrypi.stackexchange.com/a/76738
    '''
    def __init__(self, button, callback, edge='both', bouncetime=100):
        super().__init__(daemon=True)
        self.__name__ = callback.__name__
        self.edge = edge
        self.callback = callback
        self.button = button
        self.bouncetime = float(bouncetime)/1000

        self.lastpinval = self.button.is_active
        self.lock = threading.Lock()

    def __call__(self, *args):
        if not self.lock.acquire(blocking=False):
            return

        t = threading.Timer(self.bouncetime, self.read, args=args)
        t.start()

    def read(self, *args):
        pinval = self.button.is_active

        if (
                ((pinval is False and self.lastpinval is True) and
                 (self.edge in ['falling', 'both'])) or
                ((pinval is True and self.lastpinval is False) and
                 (self.edge in ['rising', 'both']))
        ):
            self.callback(*args)
        else:
            pass

        self.lastpinval = pinval
        self.lock.release()


def onConfChange(button):
    if button.is_active:
        onConfPress(button)
    else:
        onConfRelease(button)

def onConfPress(button):
    print("Starting group call")
    calls.CallAll()
    # Call initiated, press again to end
    callButton.when_pressed = hangup
    # If held callback is currently set to hang up, change it back to PTT callback for next hold
    callButton.when_held = onConfHeld
    led.on()

def onConfHeld(button):
    # Entered PTT mode, change what happens when button released
    print("Entered Push-to-talk, release to hangup")
    # But first set debounceCall instance lastpinval to false when released
    debounceCall.lastpinval = False
    callButton.when_released = hangup

def onConfRelease(button):
    #print("release")
    pass

def hangup(arg):
    print("Hanging up")
    calls.Hangup()
    led.off()
    # Reset press/release callbacks
    callButton.when_pressed = debounceCall
    callButton.when_released = debounceCall
    # Prevent "onConfHeld" callback from starting PTT (will reset on next press)
    callButton.when_held = None

def reset(arg):
    print("Called reset")
    calls.Reset()

# Debounce invocations of onConfChange
debounceCall = ButtonHandler(callButton, onConfChange, edge='both')
callButton.when_pressed = debounceCall
callButton.when_released = debounceCall

callButton.hold_time = 1
# Already debounced based on hold_time
callButton.when_held = onConfHeld

# Number of times pressed and length of time pressed don't matter here
resetButton.when_pressed = reset

# TODO: see if there's a better way to keep this running
while True:
    time.sleep(1)
