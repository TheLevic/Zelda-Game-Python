from posixpath import islink
import pygame
import time

from pygame.locals import*
from time import sleep

class Sprite():
	x = 0;
	y = 0;
	w = 0;
	h = 0;
	isActive = True;
	def __init__(self):
		self.x = 0;
		self.y = 0;
		self.w = 0;
		self.h = 0;
		self.isActive = True;
	
	def draw(self):
		pass
	def update(self):
		pass
	def loadImage(self):
		pass
	def Collided(self):
		pass
	def isBrick(self):
		return False;
	def isLink(self):
		return False
	def isBoomerang(self):
		return False
	def isPot(self):
		return False


class Link(Sprite):
	
	def __init__(self):
		self.x = 100;
		self.y = 100;
		self.w = 55;
		self.h = 70;
		self.animationNum = 0;
		self.prevX = self.x;
		self.prevY = self.y;
		self.images = [];
		self.loadImage();
		self.image = self.images[self.animationNum];

	def loadImage(self):
		if (len(self.images) == 0):
			for x in range(1,25):
				self.images.append(pygame.image.load("linkPictures\\"+ str(x) + ".png"));
	def isLink(self):
		return True;



class Model():
	def __init__(self):
		self.sprites = [];
		link = Link();
		self.sprites.append(link);
		

	def update(self):
		pass
		

class View():
	def __init__(self, model):
		screen_size = (700,500)
		self.screen = pygame.display.set_mode(screen_size, 32)
		# self.turtle_image = pygame.image.load("turtle.png")
		self.model = model
		# self.model.rect = self.turtle_image.get_rect()

	def update(self):
		self.screen.fill([0,200,100])
		# self.screen.blit(self.turtle_image, self.model.rect)
		for sprite in self.model.sprites:
			self.spriteImage = sprite.image;
			self.model.rect = self.spriteImage.get_rect();
			self.screen.blit(sprite.image, (sprite.x,sprite.y));
		pygame.display.flip()

class Controller():
	def __init__(self, model):
		self.model = model
		self.keep_going = True

	def update(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_going = False
			elif event.type == pygame.MOUSEBUTTONUP:
				self.model.set_dest(pygame.mouse.get_pos())
		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			self.model.dest_x -= 1
		if keys[K_RIGHT]:
			self.model.dest_x += 1
		if keys[K_UP]:
			self.model.dest_y -= 1
		if keys[K_DOWN]:
			self.model.dest_y += 1

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)
print("Goodbye")