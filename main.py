#!/usr/bin/env python
#
# An attempt at breaking bricks
#
# Nick West, 04/09/2018

#
# Constants
#

SCREEN_HEIGHT = 480
SCREEN_WIDTH = 640
PLAYER_HEIGHT = 8
PLAYER_WIDTH = 85
PLAYER_SPEED = 5
BALL_WIDTH = 11
BALL_HEIGHT = 11
SCORE = 0
LIVES = 3

try:
  import sys
  import random
  import math
  import os
  import getopt
  import pygame
  from socket import *
  from pygame.locals import *
except ImportError as err:
  print("couldn't load module. %s" % (err))
  sys.exit(2)

def load_png(name):
  """ load image and return image object """
  fullname = os.path.join('data', name)
  try:
    image = pygame.image.load(fullname)
    if image.get_alpha is None:
      image = image.convert()
    else:
      image = image.convert_alpha()
  except pygame.error as message:
    print('Cannot load image:', fullname)
    raise SystemExit(message)
  return image, image.get_rect()

class Ball(pygame.sprite.Sprite):
  """ ball object to control movement and collision """

  def __init__(self, x, y, vector):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = load_png('ball.png')
    screen = pygame.display.get_surface()
    self.area = screen.get_rect()
    self.vector = vector
    self.hit = 0
    self.oob = False
    self.rect.x = x
    self.rect.y = y

  def calcnewpos(self,rect,vector):
    (angle,z) = vector
    (dx,dy) = (z*math.cos(angle), z*math.sin(angle))
    return rect.move(dx,dy)

  def update(self):
    newpos = self.calcnewpos(self.rect, self.vector)
    self.rect = newpos
    (angle,z) = self.vector

    # if the display screen does not contain the ball's new position
    if not self.area.contains(newpos):
      # is ball's new position topleft corner not contained in the display screen?
      tl = not self.area.collidepoint(newpos.topleft)
      tr = not self.area.collidepoint(newpos.topright)
      bl = not self.area.collidepoint(newpos.bottomleft)
      br = not self.area.collidepoint(newpos.bottomright)
      # if both ball's top right and top left corners are not in the display's area, collision with top, bounce ball horizontally
      if tr and tl:
        angle = -angle
      if tl and bl:
        angle = math.pi - angle
      if tr and br:
        angle = math.pi - angle
      if bl and br:
        self.oob = True

    # check for collision with paddle
    if self.rect.colliderect(player.rect):
      # fix ball's y
      self.rect.y = player.rect.y - self.rect.height
      # horizontal bounce
      angle = -angle
      # check for collision with bricks
      for brick in bricks:
        if self.rect.colliderect(brick.rect) == 1 and not self.hit:
          bricks.remove(brick)
          all_sprites_list.remove(brick)
          quad = ((angle*(180/math.pi))%360)//90
          bt = Rect(brick.rect.x,brick.rect.y,brick.rect.width,1)
          bb = Rect(brick.rect.x,brick.rect.y+brick.rect.height,brick.rect.width,1)
          bl = Rect(brick.rect.x,brick.rect.y,1,brick.rect.y+brick.rect.height)
          br = Rect(brick.rect.x+brick.rect.width,brick.rect.y,1,brick.rect.y+brick.rect.height)
          if self.rect.colliderect(bt):
            #handle top left corner
            if self.rect.colliderect(bl):
              #if both top and left are colliding
              print("hit brick top and left")
              #if more ball x is overlapping than ball y, horiz bounce
              if abs(self.rect.centerx - brick.rect.left) > abs(self.rect.centery - brick.rect.top):
                angle = math.pi - angle
                #reset the y position of the ball so ball is not inside the brick
                self.rect.y = brick.rect.y - self.rect.height - 1
              #if more ball y is overlapping than ball x, vert bounce
              elif abs(self.rect.centerx - brick.rect.left) < abs(self.rect.centery - brick.rect.top):
                angle = -angle
                #set the ball's x value so we are not inside the brick
                self.rect.x = brick.rect.x - self.rect.width - 1
              elif quad == 2:
                angle = angle - math.pi
                self.rect.y = brick.rect.y - self.rect.height
                self.rect.x = brick.rect.x - ball.rect.width
                print("hit brick top and left perfectly")
              else:
                angle = -angle
            #handle top right corner
            elif self.rect.colliderect(br):
              #if both top and right are colliding...
              print("hit brick top and right")
              #if more ball x overlaps brick than ball y, horiz bounce
              if abs(self.rect.centerx - brick.rect.right) > abs(self.rect.centery - brick.rect.top):
                angle = math.pi - angle
                #reset the ball's y so as to not overlap brick
                self.rect.y = brick.rect.y - self.rect.height
              #if more ball y overlaps brick than ball x, vert bounce
              elif abs(self.rect.centerx - brick.rect.right) < abs(self.rect.centery - brick.rect.top):
                angle = -angle
                #reset the ball's x so as to not overlap brick
                self.rect.x = brick.rect.right + 1
              else:
                print("hit brick top and right perfectly")
                angle = angle - math.pi
                self.rect.y = brick.rect.y - self.rect.height
                self.rect.x = brick.rect.right + 1
            else:
              angle = -angle
              self.rect.y = brick.rect.y - self.rect.height - 1
              print("hit brick top")
            self.hit = not self.hit

          if self.rect.colliderect(bb):
            #handle bottom left corner
            if self.rect.colliderect(bl):
              print("hit brick bottom and left")
              #if both bottom and left are colliding...
              #if more ball x overlaps than y, horiz bounce
              if abs(self.rect.centerx - brick.rect.left) > abs(self.rect.centery - brick.rect.bottom):
                angle = math.pi - angle
                #reset the ball's y
                self.rect.y = brick.rect.bottom + 1
              #if more ball y overlaps brick than x, vert bounce
              elif abs(self.rect.centerx - brick.rect.left) < abs(self.rect.centery - brick.rect.bottom):
                angle = -angle
                #reset ball's x
                self.rect.x = brick.rect.x - self.rect.width - 1
              else:
                print("hit brick bottom and left perfectly")
                angle = angle - math.pi
                self.rect.y = brick.rect.bottom + 1
                self.rect.x = brick.rect.x - self.rect.width - 1
            #handle bottom right corner
            elif self.rect.colliderect(br):
              print("hit brick bottom and right")
              #if both bottom and right are colliding...
              #if more ball x overlaps brick than y, horiz bounce
              if abs(self.rect.centerx - brick.rect.right) > abs(self.rect.centery - brick.rect.bottom):
                angle = math.pi - angle
                #set ball's y value
                self.rect.y = brick.rect.bottom + 1
              #if more ball y overlaps brick than ball x, vert bounce
              elif abs(self.rect.centerx - brick.rect.right) < abs(self.rect.centery - brick.rect.bottom):
                angle = -angle
                #reset ball's x
                self.rect.x = brick.rect.right + 1
              else:
                print("hit brick bottom and right perfectly")
                angle = angle - math.pi
                self.rect.x = brick.rect.right + 1
                self.rect.y = brick.rect.bottom + 1
            else:
              angle = -angle
              #reset ball's y
              self.rect.y = brick.rect.bottom + 1
              print("hit brick bottom")
              self.hit = not self.hit
              if self.rect.colliderect(br) and not self.hit:
                print("hit right")
                angle = math.pi - angle
                self.hit = not self.hit
                self.rect.x = brick.rect.right + 1
              elif self.rect.colliderect(bl) and not self.hit:
                print("hit left")
                angle = math.pi - angle
                self.hit = not self.hit
                self.rect.x = brick.rect.x - 1

    elif self.hit:
      self.hit = not self.hit

    # update the ball's vector
    self.vector = (angle,z)

class Brick(pygame.sprite.Sprite):
  """ brick object """

  def __init__(self, xxx_todo_changeme):
    (posx, posy) = xxx_todo_changeme
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = load_png('brick.png')
    self.rect.x = posx
    self.rect.y = posy    
    # call super constructor, pass in group of sprites, in this case, 'bricks'
    pygame.sprite.Sprite.__init__(self, bricks) 

class Player(pygame.sprite.Sprite):
  """ Player object """
  #constructor
  def __init__(self, x, y):
    #what the heck is this for?
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = load_png('paddle.png')
    self.rect.x = x
    self.rect.y = y
    pygame.sprite.Sprite.__init__(self, all_sprites_list)
  #paddle's move function
  def move(self, dirx):
    self.rect.x += dirx
    #make sure paddle can't go off screen
    if self.rect.x < 0:
      self.rect.x = 1
    if  self.rect.right > SCREEN_WIDTH:
      self.rect.right = SCREEN_WIDTH

#class Level(pygame.sprite.Sprite):
  # nothing for now

# define testing level
level = [
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,1,1,0,1,1,0,0,0],
  [0,0,0,1,1,1,1,1,1,1,0,0],
  [0,0,1,1,0,1,1,1,0,1,1,0],
  [0,0,1,1,1,1,1,1,1,1,1,0],
  [0,0,1,0,1,0,1,0,1,0,1,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,1,1,0,1,1,0,0,0],
  [0,0,0,1,1,1,1,1,1,1,0,0],
  [0,0,1,1,0,1,1,1,0,1,1,0],
  [0,0,1,1,1,1,1,1,1,1,1,0],
  [0,0,1,1,1,1,1,1,1,1,1,0],
  [0,0,1,0,1,0,1,0,1,0,1,0],
  [0,0,0,1,1,1,1,1,1,1,0,0]]

def make_level(level):
  """ given a matrix, make a level, starting at (0,0) """  
  for i in range(len(level)):
    for j in range(len(level[i])):
      if level[i][j] == 1:
        brick = Brick((0,0))
        brick.rect.x = (brick.rect.width + 3) * j
        brick.rect.y = (brick.rect.height + 3) * i
        bricks.add(brick)
        all_sprites_list.add(brick)

def main():
  pygame.init()
  screen = pygame.display.set_mode((640, 480))
  pygame.display.set_caption('b r i c k b r e a k e r')

  # fill background
  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill((0,0,0))

  # used for list of all sprites
  global all_sprites_list
  all_sprites_list = pygame.sprite.Group()

  # initiliaze bricks, contains all brick sprites, create Group object of bricks.
  global bricks
  bricks = pygame.sprite.Group()
  make_level(level)

  # initialize player
  global player
  player = Player((SCREEN_WIDTH / 2) - (PLAYER_WIDTH / 2), SCREEN_HEIGHT - PLAYER_HEIGHT)
  all_sprites_list.add(player)

  # initialize ball
  speed = 4
  rand = ((0.1*(random.randint(5,8))))
  ball = Ball(player.rect.centerx - (BALL_WIDTH / 2), player.rect.y - BALL_HEIGHT, (.743723, speed))
  all_sprites_list.add(ball)

  # initialize sprites
  ballsprite = pygame.sprite.RenderPlain(ball)

  # blit background to screen
  screen.blit(background, (0,0))
  pygame.display.flip()

  # initialize clock
  clock = pygame.time.Clock()

  # event loop
  while 1:
    # controls the speed at which the game run (fps)
    clock.tick(120)

    # keyboard input
    for event in pygame.event.get():
      if event.type == QUIT:
        return
    # get list of keys, handle input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
      player.move(-PLAYER_SPEED)
    if keys[pygame.K_RIGHT]:
      player.move(PLAYER_SPEED)  

    # clear screen to produce illusion of animation
    screen.fill((0,0,0))

    # blit all sprites (can we do this another way? ie, only draw sprites when they are needed?) blitting is resource intensive  
    #for sprite in all_sprites_list:
    #  screen.blit(background, sprite.rect, sprite.rect)
    # check for movement of ball
    ballsprite.update()
    if ball.oob == True:
      print("ball out of bounds. you suck")
      #lives -= 1
      #reset()
      break

    # why is this here?
    all_sprites_list.draw(screen)

    # And this?
    pygame.display.flip()

if __name__ == '__main__': main()
