from adafruit_servokit import ServoKit
from gpiozero import OutputDevice
import time

kit = ServoKit(channels=16)

class Stepper:
    def __init__(self, enablePin, directionPin, pulsePin, stepsPerRev=3200.0):
        self.stepsPerDeg = stepsPerRef/360.0
        self.enable = OutputDevice(enablePin)
        self.direction = OutputDevice(directionPin)
        self.pulse = OutputDevice(pulsePin)
        self.pos = 0
        on()

    def step(self):
        self.pulse.toggle()

    def dirPos(self):
        self.direction.on()

    def dirNeg(self):
        self.direction.off()

    def on(self):
        self.enable.on()

    def off(self): 
        self.enable.off()

    def move(self, angle):
        toMove = angle - self.pos
        if(toMove > 0):
            dirPos()
        else:
            dirNeg()
        for i in range(toMove):
            self.step()
            time.sleep(0.001)

class Servo:
    def __init__(self, n):
        self.driver = kit[n]

    def move(self, angle):
        self.driver.angle = angle



class Bot():
    def __init__(self):
        rightShoulder = Stepper(26, 19, 13)
        leftShoulder = Stepper(21, 20, 16)
        rightElbow = Servo(0)
        leftElbow = Servo(1)

bot = Bot()


        
