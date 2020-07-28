import time

from collections import OrderedDict
from gpiozero import CompositeDevice, SourceMixin, GPIOPinMissing, OutputDevice
from gpiozero import Button


class ShiftRegister(SourceMixin, CompositeDevice):
    def __init__(self, data=None, latch=None, clock=None, initial_value=None, bit_count=8, pin_factory=None):
        if not all(p is not None for p in [data, latch, clock]):
            raise GPIOPinMissing('data, latch, and clock pins must be provided')
        devices = OrderedDict((
            ('data_device', OutputDevice(data, pin_factory=pin_factory)),
            ('latch_device', OutputDevice(latch, initial_value=True, pin_factory=pin_factory)),
            ('clock_device', OutputDevice(clock, pin_factory=pin_factory)),
        ))
        self._bit_count = bit_count
        super().__init__(_order=devices.keys(), **devices)

        if initial_value is None:
            initial_value = int('0' * self.bit_count, 2)
        self.value = initial_value

    @property
    def bit_count(self):
        return self._bit_count

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._shift_out(value)
        self._value = value

    def on(self, bit):
        self.value |= 1 << bit

    def off(self, bit):
        self.value &= ~(1 << bit)

    def toggle(self, bit):
        self.value ^= 1 << bit

    def _shift_out(self, value):
        self.latch_device.off()
        for x in range(self.bit_count):
            self.data_device.value = (value >> x) & 1
            self.clock_device.off()
            self.clock_device.on()
            self.clock_device.off()
        self.latch_device.on()
        self.latch_device.off()
        self.data_device.off()

#register = ShiftRegister(data=4, latch=6, clock=5)
#black = Button(26)
#red = Button(10)
#while True:
#    if black.is_pressed:
#        register.on(7)
#        register.off(6)
#    else:
#        register.off(7)
#        register.on(6)
#    if red.is_pressed:
#        register.on(5)
#        register.off(4)
#    else:
#        register.off(5)
#        register.on(4)
#    time.sleep(.2)

#register = ShiftRegister(data=4, latch=6, clock=5)
##register.on(7)
#print(register.value)
#time.sleep(2)
#register.on(6)
#print(register.value)
#time.sleep(1)
#register.on(5)
#print(register.value)
#time.sleep(1)
#register.on(4)
#print(register.value)
#time.sleep(1)
#register.on(3)
#print(register.value)
#time.sleep(1)
#register.off(5)
#print(register.value)
#time.sleep(1)
#register.value = 0
#time.sleep(5)
