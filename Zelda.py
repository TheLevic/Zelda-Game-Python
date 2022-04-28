from posixpath import islink
import pygame
import time

from pygame.locals import*
from time import sleep

class Sprite():
	def __init__(self):
		self.x = 0
		self.y = 0
		self.w = 0
		self.h = 0
		self.isActive = True
	
	def draw(self):
		pass
	def update(self):
		pass
	def loadImage(self):
		pass
	def Collided(self):
		pass
	def isBrick(self):
		return False
	def isLink(self):
		return False
	def isBoomerang(self):
		return False
	def isPot(self):
		return False


class Link(Sprite):
	
	def __init__(self):
		self.x = 100
		self.y = 100
		self.w = 55
		self.h = 70
		self.speed = 5
		self.animationNum = 0
		self.prevX = self.x
		self.prevY = self.y
		self.images = []
		self.loadImage()
		self.image = self.images[self.animationNum]
		self.direction = 0

	def loadImage(self):
		if (len(self.images) == 0):
			for x in range(1,25):
				self.images.append(pygame.image.load("linkPictures/"+ str(x) + ".png"))



	def isLink(self):
		return True

	def update():
		return True

	def getOutOfSprite(self, b):
		if self.x + self.w >= b.x and self.prevX + self.w <= b.x:
			self.x = self.prevX
		if self.x <= b.x + b.w and self.prevX >= b.x + b.w:
			self.x = self.prevX
		if self.y <= b.y + b.h and self.prevY >= b.y + b.h:
			self.y = self.prevY
		if self.y + self.h >= b.y and self.prevY + self.h <= b.y:
			self.y = self.prevY

	def savePrev(self):
		self.prevX = self.x
		self.prevY = self.y

	def getDirection(self):
		return self.direction

	# Link's movement
	def moveUp(self):
		self.direction = 1
		self.y -= self.speed
		if self.animationNum >= 4:
			self.animationNum = 0	
		self.image = self.images[self.animationNum]
		self.animationNum += 1

	def moveDown(self):
		self.direction = 3
		self.y += self.speed
		if self.animationNum >= 9 or self.animationNum < 5:
			self.animationNum = 5
		self.image = self.images[self.animationNum]
		self.animationNum += 1

	def moveRight(self):
		self.direction = 2
		self.x += self.speed
		
		if self.animationNum >= 19 or self.animationNum < 15:
			self.animationNum = 15
		self.image = self.images[self.animationNum]
		self.animationNum += 1

	def moveLeft(self):
		self.direction = 4
		self.x -= self.speed
		if self.animationNum >= 14 or self.animationNum < 10:
			self.animationNum = 10
		self.image = self.images[self.animationNum]
		self.animationNum += 1

class Brick(Sprite):
	def __init__(self,locationx,locationy):
		self.image = pygame.image.load("brick.jpg")
		self.x = locationx
		self.y = locationy
		self.w = 50
		self.h = 50
	def update(self):
		return True
	def Collided(self):
		pass


class Model():
	def __init__(self):
		self.sprites = []
		self.link = Link()
		self.brick1 = Brick(400,400)
		self.sprites.append(self.link)
		self.sprites.append(self.brick1)
		

	def update(self):
		pass
		

class View():
	def __init__(self, model):
		screen_size = (700,500)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.model = model

	def update(self):
		self.screen.fill([0,200,100])
		# self.screen.blit(self.turtle_image, self.model.rect)
		for sprite in self.model.sprites:
			self.spriteImage = sprite.image
			self.model.rect = self.spriteImage.get_rect()
			self.screen.blit(sprite.image, (sprite.x,sprite.y))
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
				if event.key == K_q:
					self.keep_going = False
		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			self.model.link.moveLeft()
		if keys[K_RIGHT]:
			self.model.link.moveRight()
		if keys[K_UP]:
			self.model.link.moveUp()
		if keys[K_DOWN]:
			self.model.link.moveDown()




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