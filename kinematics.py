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

PX_PER_CM = 10
WINDOW_HEIGHT_CM =1 
WINDOW_WIDTH_CM =1 
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

class Bot:
    def __init__(self):
        self.left_arm = Chain(name='left_arm', links = [
            OriginLink(),
            URDFLink(
                name="shoulder",
                translation_vector=[-8, 0, 0],
                orientation=[0, 0, math.radians(-30)],
                rotation=[0, 0, 1],
            ),
            URDFLink(
                name="backarm",
                translation_vector=[-15,0,0],
                orientation=[0,0,math.radians(-90)],
                rotation=[0,0,1]
            ),
            URDFLink(
                name="forearm",
                translation_vector=[-15,0,0],
                orientation=[0,0,0],
                rotation=[0,0,1]
                )
        ])

        self.right_arm = Chain(name='right_arm', links = [
            OriginLink(),
            URDFLink(
                name="shoulder",
                translation_vector=[8, 0, 0],
                orientation=[0, 0, math.radians(30)],
                rotation=[0, 0, 1],
            ),
            URDFLink(
                name="backarm",
                translation_vector=[15,0,0],
                orientation=[0,0,math.radians(90)],
                rotation=[0,0,1]
            ),
            URDFLink(
                name="forearm",
                translation_vector=[15,0,0],
                orientation=[0,0,0],
                rotation=[0,0,1]
                )
        ])


    def render(self):
        pass

    def step(self):
        pass

    
class Book:
    def __init__(self):
        pass
    def render(self):
        pass

def run():

    clock = pygame.time.Clock()

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

    last_render = pygame.time.get_ticks()
    # run the game loop
    ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')
    ax.set(xlim=(-30,30), ylim=(-30,30))
    bot.left_arm.plot([0,0,0,0], ax)
    bot.right_arm.plot([0,0,0,0], ax)

    matplotlib.pyplot.show()

    while True:
        clock.tick(60)
        windowSurface.fill(WHITE)
        bot.step()
        book.render()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

run()
