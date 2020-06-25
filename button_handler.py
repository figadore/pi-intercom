#!/usr/bin/env python3
'''
Single button controls call functionality. Short press opens
all-way communications for hands-free mode. Next press closes the line.
Alternatively, long-pressing the button enables push-to-talk mode,
closing the line when the button is released
'''
import os
import time
import threading

import intercom
import jamid
from gpiozero import LED, Button

#led = LED(4)
call_button = Button(26)
reset_button = Button(17)
mgr = {}

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


def on_conf_change(button):
    if button.is_active:
        on_conf_press(button)
    else:
        on_conf_release(button)

def on_conf_press(button):
    print("Starting group call")
    mgr.call_all()
    # Call initiated, press again to end
    call_button.when_pressed = hangup_all
    # If held callback is currently set to hang up, change it back to PTT callback for next hold
    call_button.when_held = on_conf_held
    #led.on()

def on_conf_held(button):
    # Entered PTT mode, change what happens when button released
    print("Entered Push-to-talk, release to hangup")
    # But first set debounce_call instance lastpinval to false when released
    debounce_call.lastpinval = False
    call_button.when_released = hangup_all

def on_conf_release(button):
    #print("release")
    pass

def hangup_all(arg):
    print("Hanging up")
    mgr.hangup_all()
    #led.off()
    # Reset press/release callbacks
    call_button.when_pressed = debounce_call
    call_button.when_released = debounce_call
    # Prevent "on_conf_held" callback from starting PTT (will reset on next press)
    call_button.when_held = None

def reset(arg):
    print("Called reset")
    jamid.reset()
    mgr = intercom.Intercom()

if __name__ == "__main__":
    if not jamid.is_daemon_running():
        jamid.start_daemon(debug=True)

    # Debounce invocations of on_conf_change
    mgr = intercom.Intercom()
    mgr.start()
    print("intercom manager started")
    debounce_call = ButtonHandler(call_button, on_conf_change, edge='both')
    call_button.when_pressed = debounce_call
    call_button.when_released = debounce_call

    call_button.hold_time = 1
    # Already debounced based on hold_time
    call_button.when_held = on_conf_held

    # Number of times pressed and length of time pressed don't matter here
    reset_button.when_pressed = reset

    # TODO: see if there's a better way to keep this running
    while True:
        time.sleep(1)
