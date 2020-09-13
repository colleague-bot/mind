import pygame, sys
import math
import pygame.time
from pygame.locals import *
from collections import deque

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

class LinearProcedure:
    def __init__(self,link, angle_delta, step_delta):
        self.steps = []
        angle_step_size = angle_delta / step_delta
        for i in range(step_delta-1):
            self.steps.append((lambda: link.joint.move(angle_step_size)))
        # Last step should move the remainder, it may not be a whole number
        self.steps.append((lambda: link.joint.move(angle_delta-angle_step_size*(step_delta-1))))
        
    def get_moves(self):
        return self.steps

class Joint:
    def __init__(self, parent, child, start_angle):
        self.start_angle = start_angle
        self.parent = parent
        self.child = child
        self.angle = 0

    def dumb_move_impl(self, angle):
        self.child.angle += angle
        self.child.update_origin()
        for child in self.child.children:
            child.joint.move(angle)

    def move (self, angle):
        self.angle = (self.angle + angle) % 360
        self.dumb_move_impl(angle)
        
class Link:
    def __init__(self, length, angle):
        self.length = length
        self.angle = angle
        self.children = []

    def update_origin(self):
        self.origin = LinkStart(self, self.parent, self.parent_offset_percentage, self.child_offset_percentage)

    def joint(self, link, parent_offset_percentage=1, child_offset_percentage=0):
        self.parent = link
        self.parent_offset_percentage = parent_offset_percentage
        self.child_offset_percentage = child_offset_percentage
        self.update_origin()
        self.joint = Joint(link, self, 0)
        self.parent.children.append(self)
        return self

    def getStartOffset(self, percentage):
        return (self.length * math.cos(self.angle_rad()) * percentage * -1 * PX_PER_CM,
                self.length * math.sin(self.angle_rad()) * percentage * 1 * PX_PER_CM)

    def root(self, x, y):
        self.origin = PointStart(x, y)
        return self

    def angle_rad(self):
        return math.radians(self.angle)

    def get_end(self):
        return (self.length * math.cos(self.angle_rad())*PX_PER_CM + self.get_origin()[0], -1*self.length * math.sin(self.angle_rad())*PX_PER_CM + self.get_origin()[1])

    def get_origin(self):
        rv = self.origin.getPx()
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
        self.steps = deque()

    def next_step(self):
        if(len(self.steps) > 0):
            return self.steps.popleft()
        else:
            return []

    def add_moves(self, moves, step_ind):
        if (len(self.steps) < step_ind + 1 + len(moves)):
            for i in range(step_ind+1+len(moves) - len(self.steps)):
                self.steps.append([])

        for i in range(len(moves)):
            self.steps[i+step_ind].append(moves[i])
        
    def step(self):
        moves = self.next_step()
        for move in moves:
            move()
        self.render()

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

    turn_left_hand_match_book = LinearProcedure(bot.left_wrist, -30, 20)
    turn_right_hand_match_book = LinearProcedure(bot.right_wrist, 30, 20)

    bot.add_moves(turn_right_hand_match_book.get_moves(), 0)
    bot.add_moves(turn_left_hand_match_book.get_moves(), 0)

    last_render = pygame.time.get_ticks()
    # run the game loop
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
