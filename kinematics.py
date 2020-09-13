import pygame, sys
import math
import pygame.time
from pygame.locals import *
from collections import deque
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D
import math
import time

PX_PER_CM = 20
ORIGIN_OFFSET_X = 25
ORIGIN_OFFSET_Y = 5
WINDOW_HEIGHT_CM = 50
WINDOW_WIDTH_CM = 50
WINDOW_HEIGHT_PX = WINDOW_HEIGHT_CM * PX_PER_CM
DISTANCE_FROM_BOOK = 15
# set up pygame
pygame.init()

# set up the window
windowSurface = pygame.display.set_mode((WINDOW_WIDTH_CM * PX_PER_CM, WINDOW_HEIGHT_CM * PX_PER_CM), 0, 32)
pygame.display.set_caption('Hello world!')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Arm:
    def __init__(self, direction):
        self.state = [0,0,0,0]
        if direction == "left":
            sign = -1
        else:
            sign = 1
        self.chain = Chain(name=direction + "_arm", links = [
            OriginLink(),
            URDFLink(
                name="shoulder",
                translation_vector=[8 * sign, 0, 0],
                orientation=[0, 0, math.radians(30 * sign)],
                rotation=[0, 0, 1],
            ),
            URDFLink(
                name="backarm",
                translation_vector=[16 * sign,0,0],
                orientation=[0,0,math.radians(90 * sign)],
                rotation=[0,0,1]
            ),
            URDFLink(
                name="forearm",
                translation_vector=[16 * sign,0,0],
                orientation=[0,0,0],
                rotation=[0,0,1]
                )
        ])

    def get_positions(self):
        rv = []
        positions = self.chain.forward_kinematics(self.state, full_kinematics=True)
        for position in positions[1:]:
            xyEtc = position[:,3]
            x = xyEtc[0]
            y = xyEtc[1]
            rv.append((x,y))
        return rv

    def go_directly_to_position(self, x, y):
        joint_positions = self.chain.inverse_kinematics(target_position=[x,y,0], target_orientation=[0,0,0])
        self.state = joint_positions
    
    def render(self):
        positions = self.get_positions()
        lastX = 0 + ORIGIN_OFFSET_X 
        lastY = 0 + ORIGIN_OFFSET_Y
        for position in positions:
            x = position[0] + ORIGIN_OFFSET_X
            y = position[1] + ORIGIN_OFFSET_Y
            pygameLastX = lastX * PX_PER_CM 
            pygameLastY = WINDOW_HEIGHT_PX - lastY * PX_PER_CM  
            pygameX = x * PX_PER_CM 
            pygameY = WINDOW_HEIGHT_PX - y * PX_PER_CM
            pygame.draw.line(windowSurface, BLUE, (pygameLastX, pygameLastY), (pygameX, pygameY))
            lastX = x 
            lastY = y


class Bot:
    def __init__(self):
        self.left_arm = Arm("left")
        self.right_arm = Arm("right")

    def get_positions(self):
        rv = []
        positions = self.left_arm.get_positions()
        
    def render(self):
        self.left_arm.render()
        self.right_arm.render()
   
    def step(self):
        pass

    def plot(bot):
        ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')
        ax.set(xlim=(-30,30), ylim=(-30,30))
        bot.left_arm.chain.plot([0,0,0,0], ax)
        bot.right_arm.chain.plot([0,0,0,0], ax)

class Book:
    def __init__(self, depth):
        self.depth = depth
        self.openness = 90
        self.center_x_cm = ORIGIN_OFFSET_X
        self.center_y_cm = WINDOW_HEIGHT_CM - ORIGIN_OFFSET_Y - DISTANCE_FROM_BOOK - self.depth
        self.compute_positions()

    def compute_positions(self):

        deg_off = self.openness/2
        self.x_left = (self.center_x_cm - math.sin(math.radians(deg_off))*self.depth)
        self.y_left = (self.center_y_cm + math.cos(math.radians(deg_off))*self.depth)
        self.x_right = (self.center_x_cm + math.sin(math.radians(deg_off))*self.depth)
        self.y_right = (self.center_y_cm + math.cos(math.radians(deg_off))*self.depth)

        self.x_left_kin = self.x_left - self.center_x_cm
        self.y_left_kin = WINDOW_HEIGHT_CM - self.y_left - ORIGIN_OFFSET_Y
        self.x_right_kin = self.x_right - self.center_x_cm
        self.y_right_kin = WINDOW_HEIGHT_CM - self.y_right - ORIGIN_OFFSET_Y

    def render(self):
        self.compute_positions()

        x_center = int(self.center_x_cm * PX_PER_CM)
        y_center = int(self.center_y_cm * PX_PER_CM)
        depth_px = int(self.depth * PX_PER_CM)

        x_left_px = int(self.x_left * PX_PER_CM)
        y_left_px = int(self.y_left * PX_PER_CM)
        x_right_px = int(self.x_right * PX_PER_CM)
        y_right_px = int(self.y_right * PX_PER_CM)

        pygame.draw.circle(windowSurface, RED, (x_center, y_center), depth_px, 4)
        pygame.draw.line(windowSurface, GREEN, (x_center, y_center), (x_left_px, y_left_px), 4)
        pygame.draw.line(windowSurface, GREEN, (x_center, y_center), (x_right_px, y_right_px), 4)

def run():

    clock = pygame.time.Clock()

    # set up fonts
    basicFont = pygame.font.SysFont(None, 48)
    
    # draw the white background onto the surface
    windowSurface.fill(WHITE)

    bot = Bot()
    bot.render()

    book = Book(15)
    book.render()

    # draw the window onto the screen
    pygame.display.update()

    bot.left_arm.go_directly_to_position(4, 40)
    
    last_render = pygame.time.get_ticks()
    # run the game loop
    matplotlib.pyplot.show()

    book_direction = 1
    while True:
        clock.tick(60)
        if(book.openness == 5 or book.openness == 160):
            book_direction *= -1

        book.openness += book_direction
        book.compute_positions()
        bot.left_arm.go_directly_to_position(book.x_left_kin, book.y_left_kin)
        bot.right_arm.go_directly_to_position(book.x_right_kin, book.y_right_kin)
        
        windowSurface.fill(WHITE)
        bot.render()
        book.render()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

run()
