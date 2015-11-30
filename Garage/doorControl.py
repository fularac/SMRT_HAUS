import RPi.GPIO as io
from time import sleep
DoorPin = 12
ButtonPressTime = .5

def init():
    io.setmode(io.BOARD)
    io.setup(DoorPin, io.OUT)
    io.output(DoorPin, io.LOW)

def HitButton():
    # Activate Relay to 'press button'
    io.output(DoorPin, io.HIGH)
    # Wait 'Human time'
    sleep(ButtonPressTime)
    # Deactivate relay to 'release button'
    io.output(DoorPin,io.LOW)
