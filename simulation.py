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
        self.child = child
        

    def getPx(self):
        end = self.link.get_end()
        origin = self.link.get_origin()
        child_start_offset = self.child.getStartOffset(self.offset_percentage[1])

        return ((end[0]-origin[0])*self.offset_percentage[0] + origin[0] + child_start_offset[0], 
                (end[1]-origin[1])*self.offset_percentage[0] + origin[1] + child_start_offset[1])

class Link:
    def __init__(self, length, angle):
        self.length = length
        self.angle = angle

    def joint(self, link, parent_offset_percentage=1, child_offset_percentage=0):
        self.origin = LinkStart(self, link, parent_offset_percentage, child_offset_percentage)
        return self

    def getStartOffset(self, percentage):
        return (self.length * math.cos(self.angle_rad()) * percentage * -1 * PX_PER_CM,
                self.length * math.sin(self.angle_rad()) * percentage * -1 * PX_PER_CM)

    def root(self, x, y):
        self.origin = PointStart(x, y)
        return self

    def angle_rad(self):
        return math.radians(self.angle)

    def get_end(self):
        return (self.length * math.cos(self.angle_rad())*PX_PER_CM + self.get_origin()[0], -1*self.length * math.sin(self.angle_rad())*PX_PER_CM + self.get_origin()[1])

    def get_origin(self):
        rv = self.origin.getPx()
        print(rv)
        return self.origin.getPx()

    def render(self, color=BLUE):
        pygame.draw.line(windowSurface, color, self.get_origin(), self.get_end(), 2)

class Bot:
    def __init__(self):
        self.root = Link(15, 0).root(WINDOW_WIDTH_CM/2-15/2, WINDOW_HEIGHT_CM-5)
        self.left_backarm = Link(15, 180-60).joint(self.root, 0)
        self.right_backarm = Link(15, 60).joint(self.root)
        self.left_forearm = Link(15,  60).joint(self.left_backarm)
        self.right_forearm = Link(15, 180-60).joint(self.right_backarm)
        self.left_wrist = Link(5, 0).joint(self.left_forearm, 1, 0.5)
        self.right_wrist = Link(5,  180).joint(self.right_forearm, 1, 0.5)
        self.left_fingers = Link(3, 90).joint(self.left_wrist, 0)
        self.right_fingers = Link(3, 90).joint(self.right_wrist, 0)
        self.left_thumb = Link(2, 90).joint(self.left_wrist)
        self.right_thumb = Link(2, 90).joint(self.right_wrist)
        


    def render(self):
        self.root.render()
        self.left_backarm.render()
        self.right_backarm.render()
        self.left_forearm.render()
        self.right_forearm.render()
        self.left_wrist.render()
        self.right_wrist.render()
        self.left_fingers.render()
        self.right_fingers.render()
        self.left_thumb.render()
        self.right_thumb.render()

class Book:
    def __init__(self):
        self.right_page = Link(15, -60).root(WINDOW_WIDTH_CM/2, 5)
        self.left_page = Link(15, -120).joint(self.right_page, 0)

    def render(self):
        self.right_page.render(RED)
        self.left_page.render(RED)

def run():

    # set up fonts
    basicFont = pygame.font.SysFont(None, 48)
    
    # draw the white background onto the surface
    windowSurface.fill(WHITE)

    bot = Bot()
    bot.render()

    book = Book()
    book.render()

    # draw the window onto the screen
    pygame.display.update()

    # run the game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

run()
