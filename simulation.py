import pygame, sys
import math
from pygame.locals import *

PX_PER_CM = 10
WINDOW_HEIGHT_CM = 50
WINDOW_WIDTH_CM = 60
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


class Start:
    def getPx():
        print("getPx not implemented")
        assert(false)

class PointStart(Start):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def getPx(self):
        return (self.x * PX_PER_CM, self.y * PX_PER_CM)

class LinkStart(Start):
    def __init__(self, child, link, parent_offset_percentage=1, child_offset_percentage=0):
        self.link = link 
        self.offset_percentage = (parent_offset_percentage, child_offset_percentage)
        

    def getPx(self):
        end = self.link.get_end()
        origin = self.link.get_origin()

        return ((end[0]-origin[0])*self.offset_percentage[0] + origin[0], 
                (end[1]-origin[1])*self.offset_percentage[0] + origin[1])

class Link:
    def __init__(self, length, angle):
        self.length = length
        self.angle = angle

    def joint(self, link, parent_offset_percentage=1, child_offset_percentage=0):
        self.origin = LinkStart(self, link, parent_offset_percentage, child_offset_percentage)
        return self

    def root(self, x, y):
        self.origin = PointStart(x, y)
        return self

    def angle_rad(self):
        return math.radians(self.angle)

    def get_end(self):
        return (self.length * math.cos(self.angle_rad())*PX_PER_CM + self.get_origin()[0], -1*self.length * math.sin(self.angle_rad())*PX_PER_CM + self.get_origin()[1])

    def get_origin(self):
        return self.origin.getPx()

    def render(self):
        pygame.draw.line(windowSurface, BLUE, self.get_origin(), self.get_end(), 2)

def run():

    # set up fonts
    basicFont = pygame.font.SysFont(None, 48)
    
    # draw the white background onto the surface
    windowSurface.fill(WHITE)

    root = Link(15, 0).root(WINDOW_WIDTH_CM/2-15/2, WINDOW_HEIGHT_CM-5)
    left_backarm = Link(15, 180-60).joint(root, 0.0)
    right_backarm = Link(15, 60).joint(root)
    left_forearm = Link(15,  60).joint(left_backarm)
    right_forearm = Link(15, 180-60).joint(right_backarm)
    left_wrist = Link(5, 0).joint(left_forearm, 1, 0.5)
    right_wrist = Link(5,  180).joint(right_forearm, 1, 0.5)

    root.render()
    left_backarm.render()
    right_backarm.render()
    left_forearm.render()
    right_forearm.render()
    left_wrist.render()
    right_wrist.render()

    # draw the window onto the screen
    pygame.display.update()

    # run the game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

run()
