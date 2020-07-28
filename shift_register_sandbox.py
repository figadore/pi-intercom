import gpiozero
import argparse
import time

shift_pin = gpiozero.OutputDevice(5)
reset_pin = gpiozero.OutputDevice(9)
store_pin = gpiozero.OutputDevice(6)
data_pin = gpiozero.OutputDevice(4)
data_led = gpiozero.LED(25)
#output_pin = gpiozero.OutputDevice(10)

def reset():
    reset_pin.off()
    time.sleep(.1)
    reset_pin.on()

def shift():
    shift_pin.off()
    #time.sleep(.1)
    shift_pin.on()

def store():
    store_pin.off()
    #time.sleep(.1)
    store_pin.on()

def toggle_output():
    output_pin.toggle()

def toggle_data():
    print("toggle data")
    data_pin.toggle()
    data_led.toggle()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    #output_pin.off() #enable output on low
    #reset_pin.on() #resets on low

    parser.add_argument('--reset', action='store_true')
    parser.add_argument('--shift', action='store_true')
    parser.add_argument('--store', action='store_true')
    parser.add_argument('--toggle-output', action='store_true')
    parser.add_argument('--toggle-data', action='store_true')
    args = parser.parse_args()

    if args.reset:
        reset()

    if args.shift:
        shift()

    if args.store:
        store()

    if args.toggle_output:
        toggle_output()

    if args.toggle_data:
        toggle_data()

    reset()
    toggle_data()
    shift()
    store()
    print("store")
    #time.sleep(3)
    #toggle_data()
    ##toggle_data()
    #shift()
    #store()
    #print("store")
    #time.sleep(3)
    #toggle_data()
    #shift()
    #store()
    #print("store")
    ##toggle_output()
    #time.sleep(1)
    ##toggle_data()
    #shift()
    #store()
    #print("store")
    #time.sleep(1)
    ##toggle_data()
    #shift()
    #store()
    #print("store final")
    #toggle_output()
    time.sleep(1)
    print("done")
