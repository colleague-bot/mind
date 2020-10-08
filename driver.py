from adafruit_servokit import ServoKit
from gpiozero import OutputDevice
import time
from threading import Thread

kit = ServoKit(channels=16)

class Stepper:
    def __init__(self, enablePin, directionPin, pulsePin, stepsPerRev=3200.0):
        self.stepsPerDeg = stepsPerRev/360.0
        self.enable = OutputDevice(enablePin)
        self.direction = OutputDevice(directionPin)
        self.pulse = OutputDevice(pulsePin)
        self.pos = 0
        self.on()

    def step(self):
        self.pulse.toggle()

    def dirPos(self):
        self.direction.on()

    def dirNeg(self):
        self.direction.off()

    def on(self):
        # 0 is on
        self.enable.off()

    def off(self): 
        # 1 is off
        self.enable.on()

    def move(self, angle):
        print("moving")
        toMove = angle - self.pos
        if(toMove > 0):
            self.dirPos()
        else:
            self.dirNeg()
            toMove = -toMove
        for i in range(int(toMove*self.stepsPerDeg) * 2):
            self.step()
            time.sleep(0.001)

class Servo:
    def __init__(self, n):
        self.driver = kit.servo[n]

    def move(self, angle):
        self.driver.angle = angle



class Bot():
    def __init__(self):
        self.rightShoulder = Stepper(26, 19, 13)
        self.leftShoulder = Stepper(21, 20, 16)
        self.rightElbow = Servo(0)
        self.rightElbow.move(180)
        self.leftElbow = Servo(1)
        self.leftElbow.move(0)
        self.headZ = Servo(2)
        self.headZ.move(90)
        self.headY = Servo(3)
        self.headY.move(90)
        self.rightFingers = Servo(6)
        self.rightFingers.move(180)
        self.rightThumb = Servo(7)
        self.rightThumb.move(180)
        self.leftWrist = Servo(5)
        self.leftWrist.move(180)
        self.rightWrist = Servo(4)
        

    def die(self):
        self.rightShoulder.off()
        self.leftShoulder.off()


bot = Bot()

def dance():
    for i in range(20):
        if(i%2 == 0):
            Thread(target = lambda: bot.rightShoulder.move(38)).start()
            Thread(target = lambda: bot.rightElbow.move(180-30)).start()
            Thread(target = lambda: bot.leftElbow.move(30)).start()
            bot.leftShoulder.move(-38)
        else:
            Thread(target = lambda: bot.rightShoulder.move(-38)).start()
            Thread(target = lambda: bot.rightElbow.move(180)).start()
            Thread(target = lambda: bot.leftElbow.move(0)).start()
            bot.leftShoulder.move(38)


        
