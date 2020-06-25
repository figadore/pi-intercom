'''
Stores call details for intercom stations, manages indicators (LEDs)
'''
import socket
from gpiozero import LED

class Station():
    def __init__(self, display_name, device_type, username, ip, sip_domain="", led_pin1=None, led_pin2=None):
        self.sip_domain = sip_domain
        self.ip = ip
        self.display_name = display_name
        self.device_type = device_type
        self.username = username
        self.station_status = ""
        self.led1 = None
        self.led2 = None
        self.call_id = None
        if led_pin1 is not None:
            self.led1 = LED(led_pin1)
            print("set up led1")
        else:
            print("no led to set up")
        if led_pin2 is not None:
            if led_pin2 == led_pin1:
                self.led2 = self.led1
            else:
                self.led2 = LED(led_pin2)
            print("set up led2")

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

    def set_call_id(self, call_id):
        self.call_id = call_id

    def get_call_id(self):
        return self.call_id

    def set_call_status(self, status):
        print("station setting call status")
        self.call_status = status
        if status == "HUNGUP":
            self.led_off()
        elif status == "CONNECTING":
            self.led_blink_slow()
        elif status == "RINGING":
            self.led_blink_fast()
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
            self.call_id = None
        elif status == "INACTIVE":
            print("state inactive")
        else:
            print("unknown status:" + str(status))

    def get_call_status(self, status):
        return self.call_status

    def led_on(self):
        print("led on")
        if self.led1 is not None:
            self.led1.on()
            self.led2.off()
        else:
            print("led not found")

    def led_off(self):
        print("led off")
        if self.led1 is not None:
            self.led1.off()
            self.led2.off()
        else:
            print("led not found")

    def led_blink_fast(self):
        print("led blink")
        if self.led1 is not None:
            self.led1.off()
            self.led2.blink(on_time=.1, off_time=.1)
        else:
            print("led not found")

    def led_blink_slow(self):
        print("led blink")
        if self.led1 is not None:
            self.led1.off()
            self.led2.blink(on_time=.5, off_time=.5)
        else:
            print("led not found")
