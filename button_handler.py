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
import signal

import intercom
import jamid
from gpiozero import LED, Button


class Debouncer(threading.Thread):
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

class Handler():
    def on_conf_change(self, button):
        if button.is_active:
            self.on_conf_press(button)
        else:
            self.on_conf_release(button)

    def on_conf_press(self, button):
        print("Starting group call")
        mgr.call_all()
        # Call initiated, press again to end
        call_button.when_pressed = self.hangup_all
        # If held callback is currently set to hang up, change it back to PTT callback for next hold
        call_button.when_held = self.on_conf_held
        #led.on()

    def on_conf_held(self, button):
        # Entered PTT mode, change what happens when button released
        print("Entered Push-to-talk, release to hangup")
        # But first set debounce_call instance lastpinval to false when released
        debounce_call.lastpinval = False
        call_button.when_released = self.hangup_all

    def on_conf_release(self, button):
        #print("release")
        pass

    def hangup_all(self, arg):
        print("Hanging up")
        mgr.hangup_all()
        self.reset_buttons()

    def reset_buttons(self):
        print("resetting buttons")
        # Reset press/release callbacks
        call_button.when_pressed = debounce_call
        call_button.when_released = debounce_call
        # Prevent "on_conf_held" callback from starting PTT (will reset on next press)
        call_button.when_held = None

    def reset(self, arg):
        print("Called reset")
        jamid.reset()
        mgr = intercom.Intercom(self)

if __name__ == "__main__":
    call_button = Button(26)
    reset_button = Button(17)

    if not jamid.is_daemon_running():
        jamid.start_daemon(debug=True)

    # Debounce invocations of on_conf_change
    handler = Handler()
    print("intercom manager started")
    debounce_call = Debouncer(call_button, handler.on_conf_change, edge='both')
    call_button.when_pressed = debounce_call
    call_button.when_released = debounce_call

    call_button.hold_time = 1
    # Already debounced based on hold_time
    call_button.when_held = handler.on_conf_held

    # Number of times pressed and length of time pressed don't matter here
    reset_button.when_pressed = handler.reset

    # this prevents receiving the hangup invite for some reason
    mgr = intercom.Intercom(handler)
    signal.signal(signal.SIGINT, mgr.interruptHandler)
    mgr.start()
    print("run complete")
