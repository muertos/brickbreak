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
		if self.rect.colliderect(brick.rect) == 1 and not self.hit:
			quad = ((angle*(180/math.pi))%360)//90
			bt = Rect(brick.rect.x,brick.rect.y,brick.rect.width,1)
			bb = Rect(brick.rect.x,brick.rect.y+brick.rect.height,brick.rect.width,1)
			bl = Rect(brick.rect.x,brick.rect.y,1,brick.rect.y+brick.rect.height)
			br = Rect(brick.rect.x+brick.rect.width,brick.rect.y,1,brick.rect.y+brick.rect.height)
			if self.rect.colliderect(bt):
				#handle top left corner
				if self.rect.colliderect(bl):
					#if both top and left are colliding, but left moreso, bounce down
					if abs(self.rect.centerx - brick.rect.left) > abs(self.rect.centery - brick.rect.top):
						angle = math.pi - angle
					elif abs(self.rect.centerx - brick.rect.left) < abs(self.rect.centery - brick.rect.top):
						angle = -angle
					else:
						angle = angle - math.pi
				#handle top right corner
                                elif self.rect.colliderect(br):
                                        #if both top and right are colliding, but right moreso, bounce down
                                        if abs(self.rect.centerx - brick.rect.right) > abs(self.rect.centery - brick.rect.top):
                                                angle = math.pi - angle
                                        elif abs(self.rect.centerx - brick.rect.right) < abs(self.rect.centery - brick.rect.top):
                                                angle = -angle
					else:
						angle = angle - math.pi
				else:
					angle = -angle
				self.hit = not self.hit
			if self.rect.colliderect(bb):
                                #handle bottom left corner
                                if self.rect.colliderect(bl):
                                        #if both bottom and left are colliding, but left moreso, bounce up
                                        if abs(self.rect.centerx - brick.rect.left) > abs(self.rect.centery - brick.rect.bottom):
                                                angle = math.pi - angle
                                        elif abs(self.rect.centerx - brick.rect.left) < abs(self.rect.centery - brick.rect.bottom):
                                                angle = -angle
					else:
						angle = angle - math.pi
                                #handle bottom right corner
                                elif self.rect.colliderect(br):
                                        #if both bottom and right are colliding, but right moreso, bounce up
                                        if abs(self.rect.centerx - brick.rect.right) > abs(self.rect.centery - brick.rect.bottom):
                                                angle = math.pi - angle
                                        elif abs(self.rect.centerx - brick.rect.right) > abs(self.rect.centery - brick.rect.bottom):
                                                angle = -angle
					else:
						angle = angle - math.pi
                                else:
                                        angle = -angle
                                self.hit = not self.hit	
			if (self.rect.colliderect(br) or self.rect.colliderect(bl)) and not self.hit:
				angle = math.pi - angle
				self.hit = not self.hit
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
		
def load_bricks(level):
	"""returns list of bricks (x,y) coords"""
	newlevel = [0] * len(level)
	for b in range(len(level)):
		if level[b] == 1:
			#insert a brick with coords into the array
			#just drawing one line for now, keeping y=40
			newlevel[b] = Brick((62*b, 40))
	return newlevel

#class Level(pygame.sprite.Sprite):
	# nothing for now

def main():
	pygame.init()
	screen = pygame.display.set_mode((640, 480))
	pygame.display.set_caption('b r i c k b r e a k e r')

	# fill background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0,0,0))

	# initiliaze bricks
#	global brick 
	global bricks
	level = [0, 1, 0, 1, 0, 1]
#	brick = Brick((231, 300))
	bricks = load_bricks(level)
	for b in bricks:
		print b
#	print brick.rect	

	# initialize player
	# initialize ball
	speed = 3 
	rand = ((0.1*(random.randint(5,8))))
	ball = Ball((0,0), (.743723,speed))

	# initialize sprites
	ballsprite = pygame.sprite.RenderPlain(ball)
	drawbricks = []
	for i in range(len(bricks)):
		drawbricks[i] = pygame.sprite.RenderPlain(bricks[i])

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
		ballsprite.update()
		for i in range(len(drawbricks)):
			drawbricks[i].draw(screen)
		bricksprite.draw(screen)	
		pygame.display.flip()

if __name__ == '__main__': main()
