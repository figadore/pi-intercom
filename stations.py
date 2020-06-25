'''
Stores call details for intercom stations, manages indicators (LEDs)
'''
import socket
from gpiozero import LED

class Station():
    def __init__(self, display_name, device_type, username, ip, sip_domain="", led_pin=None):
        self.sip_domain = sip_domain
        self.ip = ip
        self.display_name = display_name
        self.device_type = device_type
        self.username = username
        self.station_status = ""
        self.led = None
        if led_pin is not None:
            self.led = LED(led_pin)
            print("set up led")
        else:
            print("no led to set up")

    def is_self(self):
        '''
        Determine if this station instance is this device
        '''
        return self.username == socket.gethostname()

    def set_station_status(self, status):
        # TODO implement station statuses like "active", "do not disturb", "mute playback", "mute capture"
        self.station_status = status

    def get_station_status(self, status):
        return self.station_status

    def set_call_status(self, status):
        print("station setting call status")
        self.call_status = status
        if status == "HUNGUP":
            self.led_off()
        elif status == "CONNECTING":
            self.led_blinking()
        elif status == "RINGING":
            self.led_blinking()
        elif status == "CURRENT":
            self.led_on()
        elif status == "HOLD":
            pass
        elif status == "BUSY":
            pass
        elif status == "FAILURE":
            self.led_off()
            #TODO beep or something
        elif status == "OVER":
            self.led_off()
        elif status == "INACTIVE":
            print("state inactive")
        else:
            print("unknown status:" + str(status))

    def get_call_status(self, status):
        return self.call_status

    def led_on(self):
        print("led on")
        if self.led is not None:
            self.led.on()
        else:
            print("led not found")

    def led_off(self):
        print("led off")
        if self.led is not None:
            self.led.off()
        else:
            print("led not found")

    def led_blinking(self):
        print("led blink")
        if self.led is not None:
            self.led.blink(on_time=.2, off_time=.2)
        else:
            print("led not found")
