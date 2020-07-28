'''
Stores call details for intercom stations, manages indicators (LEDs)
'''
import socket
import gpiozero
from gpiozero.pins.mock import MockFactory

import time
from shift_register import ShiftRegister

class StationStatus():

    status = None

    def set_status(self, status):
        # Ensure same status is not set multiple times
        if status == self.status:
            print("status was already " + status)
            return
        print("new status: " + status)
        self.status = status
        if status == 'connecting':
            self.connecting()
        elif status == 'ringing':
            self.ringing()
        elif status == 'connected':
            self.connected()
        elif status == 'hold':
            self.hold()
        elif status == 'disconnected':
            self.disconnected()
        elif status == 'test':
            self.test()
        elif status == 'unavailable':
            self.unavailable()

    def connecting(self):
        pass

    def ringing(self):
        pass

    def connected(self):
        pass

    def hold(self):
        pass

    def disconnected(self):
        pass

    def unavailable(self):
        pass

    def test(self):
        pass

class GpioStatus(StationStatus):
    def __init__(self, green_pin, yellow_pin):
        self.green_led = gpiozero.LED(green_pin)
        self.yellow_led = gpiozero.LED(yellow_pin)

    def connecting(self):
        self.green_led.off()
        self.yellow_led.blink(on_time=.5, off_time=.5)

    def ringing(self):
        self.green_led.off()
        self.yellow_led.blink(on_time=.2, off_time=.2)

    def connected(self):
        self.green_led.on()
        self.yellow_led.off()

    def hold(self):
        self.green_led.blink(on_time=.5, off_time=.5)
        self.yellow_led.off()

    def disconnected(self):
        self.green_led.off()
        self.yellow_led.off()

    def unavailable(self):
        self.green_led.off()
        self.yellow_led.on()

    def test(self):
        self.green_led.blink(on_time=.5, off_time=.5)
        self.yellow_led.blink(on_time=.3, off_time=.3)


class SipoLED(gpiozero.DigitalOutputDevice):
    def __init__(self, pin, shift_register):
        super().__init__(pin=pin, pin_factory=MockFactory())
        self.pin_number = pin
        self.shift_register = shift_register

    def _write(self, val):
        if self._value_to_state(val):
            self.shift_register.on(self.pin_number - 40)
        else:
            self.shift_register.off(self.pin_number - 40 )

class SipoStatus(GpioStatus):
    def __init__(self, shift_register, green_pin, yellow_pin):
        self.green_led = SipoLED(shift_register=shift_register, pin=green_pin)
        self.yellow_led = SipoLED(shift_register=shift_register, pin=yellow_pin)

class TftStatus(StationStatus):
    def __init__(self, display_name, row):
        pass

class Station():
    def __init__(self, display_name, device_type, username, ip, sip_domain="", led_pin1=None, led_pin2=None, button_pin=None, shift_register=None):
        self.sip_domain = sip_domain
        self.ip = ip
        self.display_name = display_name
        self.device_type = device_type
        self.username = username
        #self.station_status = ""
        self.call_id = None
        if self.status_type == "sipo":
            self.status_interface = SipoStatus(shift_register, green_pin=led_pin1, yellow_pin=led_pin2)
        elif self.status_type == "gpio":
            self.status_interface = GpioStatus(led_pin1, led_pin2)

    def is_self(self):
        '''
        Determine if this station instance is this device
        '''
        return self.username == socket.gethostname()

#    def set_station_status(self, status):
#        # TODO implement station statuses like "active", "do not disturb", "mute playback", "mute capture"
#        self.station_status = status
#
#    def get_station_status(self, status):
#        return self.station_status
#
    def set_call_id(self, call_id):
        self.call_id = call_id

    def get_call_id(self):
        return self.call_id

    def set_call_status(self, status):
        print("station setting call status")
        self.call_status = status
        if status == "HUNGUP":
            self.status_interface.set_status('disconnected')
        elif status == "CONNECTING":
            self.status_interface.set_status('connecting')
        elif status == "RINGING":
            self.status_interface.set_status('ringing')
        elif status == "CURRENT":
            self.status_interface.set_status('connected')
            self.led_on()
        elif status == "HOLD":
            self.status_interface.set_status('hold')
        elif status == "BUSY":
            print("unhandled state 'busy'")
            self.status_interface.set_status('unavailable')
            pass
        elif status == "FAILURE":
            print("unhandled state 'failure'")
            self.status_interface.set_status('unavailable')
            self.call_id = None
            #TODO beep or something
        elif status == "OVER":
            self.status_interface.set_status('disconnected')
            self.call_id = None
        elif status == "INACTIVE":
            print("unhandled state 'inactive'")
        else:
            print("unknown status:" + str(status))

    def get_call_status(self, status):
        return self.call_status

#if __name__ == "__main__":
#    # Test sipoled class 
#    register = ShiftRegister(data=4, latch=6, clock=5)
#    led1 = SipoLED(pin=41, shift_register=register)
#    led2 = SipoLED(pin=42, shift_register=register)
#    led3 = SipoLED(pin=43, shift_register=register)
#    led4 = SipoLED(pin=44, shift_register=register)
#    led5 = SipoLED(pin=45, shift_register=register)
#    led6 = SipoLED(pin=46, shift_register=register)
#    led7 = SipoLED(pin=47, shift_register=register)
#    led8 = SipoLED(pin=48, shift_register=register)
#    black = gpiozero.Button(26)
#    red = gpiozero.Button(10)
#    while True:
#        if black.is_pressed:
#            led7.on()
#            led6.on()
#        else:
#            led7.off()
#            led6.off()
#        if red.is_pressed:
#            led5.on()
#            led4.on()
#        else:
#            led5.off()
#            led4.off()
#        time.sleep(.2)

if __name__ == "__main__":
    # Test sipoled class 
    register = ShiftRegister(data=4, latch=6, clock=5)
    #led1 = SipoLED(pin=41, shift_register=register)
    #led2 = SipoLED(pin=42, shift_register=register)
    #led3 = SipoLED(pin=43, shift_register=register)
    led4 = SipoLED(pin=44, shift_register=register)
    led5 = SipoLED(pin=45, shift_register=register)
    #led6 = SipoLED(pin=46, shift_register=register)
    #led7 = SipoLED(pin=47, shift_register=register)
    #led8 = SipoLED(pin=48, shift_register=register)
    #black = gpiozero.Button(26)
    #red = gpiozero.Button(10)
    #while True:
    #    if black.is_pressed:
    #        led7.on()
    #        led6.on()
    #    else:
    #        led7.off()
    #        led6.off()
    #    if red.is_pressed:
    #        led5.on()
    #        led4.on()
    #    else:
    #        led5.off()
    #        led4.off()
    #    time.sleep(.2)
    status = SipoStatus(register, 47, 46)
    black = gpiozero.Button(26)
    red = gpiozero.Button(10)
    #status.set_status('ringing')
    status.set_status('test')
    while True:
        #if black.is_pressed:
        #    #status.ringing()
        #    #status.hold()
        #else:
        #    #status.set_status('connected')
        #    status.set_status('ringing')
        if red.is_pressed:
            led5.on()
            led4.on()
        else:
            led5.off()
            led4.off()
        time.sleep(.2)
