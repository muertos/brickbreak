#!/usr/bin/env python
#
# Clone of brick break game
#
# Nick West, 04/09/2018

try:
	import sys
	import random
	import math
	import os
	import getopt
	import pygame
	from socket import *
	from pygame.locals import *
except ImportError, err:
	print "couldn't load module. %s" % (err)
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
	except pygame.error, message:
		print 'Cannot load image:', fullname
		raise SystemExit, message
	return image, image.get_rect()

class Ball(pygame.sprite.Sprite):
	""" ball object to control movement and collision """

	#constructor
	def __init__(self, (xy), vector):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_png('ball.png')
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.vector = vector
		self.hit = 0
	
        def calcnewpos(self,rect,vector):
                (angle,z) = vector
                (dx,dy) = (z*math.cos(angle), z*math.sin(angle))
                return rect.move(dx,dy)

	def update(self):
		newpos = self.calcnewpos(self.rect, self.vector)
		self.rect = newpos
		(angle,z) = self.vector
	
		#check for collision with walls
		if not self.area.contains(newpos):
			tl = not self.area.collidepoint(newpos.topleft)
			tr = not self.area.collidepoint(newpos.topright)
			bl = not self.area.collidepoint(newpos.bottomleft)
			br = not self.area.collidepoint(newpos.bottomright)
			if tr and tl or (br and bl):
				angle = -angle
			if tl and bl:
				angle = math.pi - angle
			if tr and br:
				angle = math.pi - angle
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
	                                        #if both top and left are colliding....
						print "hit brick top and left"
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
							print "hit brick top and left perfectly"
						else:
							angle = -angle
	                                #handle top right corner
	                                elif self.rect.colliderect(br):
	                                    	#if both top and right are colliding...
						print "hit brick top and right"
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
							print "hit brick top and right perfectly"		
	                                                angle = angle - math.pi
							self.rect.y = brick.rect.y - self.rect.height
							self.rect.x = brick.rect.right + 1
	                                else:
	                                        angle = -angle
						self.rect.y = brick.rect.y - self.rect.height - 1
						print "hit brick top"
	                                self.hit = not self.hit

	                        if self.rect.colliderect(bb):
	                                #handle bottom left corner
	                                if self.rect.colliderect(bl):
						print "hit brick bottom and left"
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
							print "hit brick bottom and left perfectly"
	                                                angle = angle - math.pi
							self.rect.y = brick.rect.bottom + 1
							self.rect.x = brick.rect.x - self.rect.width - 1
	                                #handle bottom right corner
	                                elif self.rect.colliderect(br):
						print "hit brick bottom and right"
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
							print "hit brick bottom and right perfectly"
	                                                angle = angle - math.pi
							self.rect.x = brick.rect.right + 1
							self.rect.y = brick.rect.bottom + 1
	                                else:
	                                        angle = -angle
						#reset ball's y
						self.rect.y = brick.rect.bottom + 1
						print "hit brick bottom"
	                                self.hit = not self.hit        
	                        if self.rect.colliderect(br) and not self.hit:
					 print "hit right"
	                                 angle = math.pi - angle
	                                 self.hit = not self.hit
					 self.rect.x = brick.rect.right + 1
                                elif self.rect.colliderect(bl) and not self.hit:
                                         print "hit left"
                                         angle = math.pi - angle
                                         self.hit = not self.hit
                                         self.rect.x = brick.rect.x - 1


                	elif self.hit:
                        	self.hit = not self.hit

		self.vector = (angle,z)
		
class Brick(pygame.sprite.Sprite):
	""" brick object """
	""" much to do here """
	def __init__(self, (posx, posy)):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_png('brick.png')
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.x = posx
		self.rect.y = posy		
		# call super constructor, pass in group of sprites, in this case, 'bricks'
		pygame.sprite.Sprite.__init__(self, bricks) 
		
#class Level(pygame.sprite.Sprite):
	# nothing for now

# define testing level
global level
level = [
	[0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,1,1,0,1,1,0,0,0],
	[0,0,0,1,1,1,1,1,1,1,0,0],
	[0,0,1,1,0,1,1,1,0,1,1,0],
	[0,0,1,1,1,1,1,1,1,1,1,0],
	[0,0,1,1,1,1,1,1,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,1,1,0,0,0],
        [0,0,0,1,1,1,1,1,1,1,0,0],
        [0,0,1,1,0,1,1,1,0,1,1,0],
        [0,0,1,1,1,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,1,1,1,1,1,0],
	[0,0,0,1,1,1,1,1,1,1,0,0]]

def make_level():
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

	# used for list of all sprites including player
	global all_sprites_list
 	all_sprites_list = pygame.sprite.Group()
	
	# initiliaze bricks, contains all brick sprites, create Group object of bricks.
	global bricks
	bricks = pygame.sprite.Group()
	make_level()

	# initialize player
	
	# initialize ball
	speed = 7 
	rand = ((0.1*(random.randint(5,8))))
	ball = Ball((0,0), (.743723,speed))
	all_sprites_list.add(ball)

	# initialize sprites
	ballsprite = pygame.sprite.RenderPlain(ball)
	
	# draw brick here for now

	# blit everything to the screen
	screen.blit(background, (0,0))
	pygame.display.flip()

	# initialize clock
	clock = pygame.time.Clock()

	# event loop
	while 1:
		# make sure game does not run greater than 60 fps
		clock.tick(120)
		
		for event in pygame.event.get():
			if event.type == QUIT:
				return
		
		screen.blit(background, ball.rect, ball.rect)
		for b in bricks:
			screen.blit(background, b.rect, b.rect)
		ballsprite.update()
		all_sprites_list.draw(screen)	
		pygame.display.flip()

if __name__ == '__main__': main()
