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
	
	def update(self):
		newpos = calcnewpos(self.rect, self.vector)
		self.rect = newpos
		(angle, z) = self.vector
		
		#check for collision

class Brick(pygame.sprite.Sprite):
	""" brick object """
	""" much to do here """
