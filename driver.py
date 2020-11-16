from adafruit_servokit import ServoKit
from gpiozero import OutputDevice
import time
from threading import Thread
import sys
import atexit

kit = ServoKit(channels=16)

class Stepper:
    def __init__(self, enablePin, directionPin, pulsePin, stepsPerRev=3200.0):
        self.stepsPerDeg = stepsPerRev/360.0
        self.enable = OutputDevice(enablePin)
        self.direction = OutputDevice(directionPin)
        self.pulse = OutputDevice(pulsePin)
        self.pos = 0
        self.home = 0
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
        self.pos = self.pos + toMove
        if(toMove > 0):
            self.dirPos()
        else:
            self.dirNeg()
            toMove = -toMove
        for i in range(int(toMove*self.stepsPerDeg) * 2):
            self.step()
            time.sleep(0.001)

    def moveRelative(self, angle):
        print("pos: {}", self.pos)
        print("angle: {}", angle)
        self.move(self.home + angle)

class Servo:
    def __init__(self, n, home, limits=(0, 180)):
        self.driver = kit.servo[n]
        self.home = home
        self.moveHome()
        self.min_limit = limits[0]
        self.max_limit = limits[1]

    def move(self, angle):
        if angle < self.min_limit or angle > self.max_limit:
            print("angle, %d is outside limits (%d, %d)" % (angle, self.min_limit, self.max_limit))
            return
        self.driver.angle = angle

    def moveRelative(self, angle):
        self.move(self.home + angle)

    def moveHome(self):
        self.driver.angle = self.home



class Bot():
    def __init__(self):
        self.rightShoulder = Stepper(26, 19, 13)
        self.leftShoulder = Stepper(21, 20, 16)
        self.rightElbow = Servo(0, home=120, limits=(0, 180))
        self.leftElbow = Servo(1, home=60, limits=(0,180))
        self.rightShoulder.off()
        self.leftShoulder.off()
        print("Set shoulders at home")
        print("3")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        time.sleep(1)
        print("locking shoulders")
        self.rightShoulder.on()
        self.leftShoulder.on()
        time.sleep(1)
        print("3")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        time.sleep(1)

        Thread(target = lambda: bot.rightShoulder.move(90)).start()
        Thread(target = lambda: bot.leftShoulder.move(-90)).start()
        self.rightShoulder.move(60)
        self.leftShoulder.move(-60)
        self.rightElbow = Servo(0, home=120, limits=(0, 180))
        self.leftElbow = Servo(1, home=60, limits=(0,180))
        self.headZ = Servo(2, home=90, limits=(0, 180))
        self.headY = Servo(3, home=60, limits=(60, 180))
        self.leftFingers = Servo(6, home=180, limits=(90, 180))
        self.leftThumb = Servo(10, home=110, limits=(0, 180))
        self.leftWrist = Servo(5, home=120, limits=(0, 180))
        self.rightWrist = Servo(4, home=60, limits=(0,180))
        self.rightFingers = Servo(8, home=0, limits=(0, 115))
        self.rightThumb = Servo(9, home=90, limits=(0, 180))
        

    def die(self):
        self.rightShoulder.off()
        self.leftShoulder.off()


bot = Bot()

def at_exit():
    global bot
    bot.rightShoulder.off()
    bot.leftShoulder.off()
atexit.register(at_exit)

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


        
def read_from_stdin():
    while True:
        print("loop")
        data = sys.stdin.readline()
        pos = list(map(float, data.split(",")))
        # 0.0, -0.47200979958218836, -9.597039838836727, 0.0, 0.0, 0.47200961334342845, 9.597039606508062, 0.0
        Thread(target = lambda: bot.leftShoulder.moveRelative(pos[1])).start()
        Thread(target = lambda: bot.leftElbow.moveRelative(pos[2])).start()
        Thread(target = lambda: bot.leftWrist.moveRelative(pos[3])).start()
        Thread(target = lambda: bot.rightShoulder.moveRelative(pos[5])).start()
        Thread(target = lambda: bot.rightElbow.moveRelative(pos[6])).start()
        Thread(target = lambda: bot.rightWrist.moveRelative(pos[7])).start()


argument = "to be added"

if len(sys.argv) > 1 and sys.argv[1] == "--stdin":
    read_from_stdin()
