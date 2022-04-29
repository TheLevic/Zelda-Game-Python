from abc import abstractmethod
from contextlib import nullcontext
from posixpath import islink
import pygame
import time

from pygame.locals import*
from time import sleep

class Sprite():
	def __init__(self, locationx, locationy):
		self.x = locationx
		self.y = locationy
		self.isActive = True
		self.speed = 5

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
		super().__init__(100,100)
		self.w = 55
		self.h = 70
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

	def update(self):
		self.savePrev()
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
		super().__init__(locationx,locationy)
		self.image = pygame.image.load("brick.jpg")
		self.w = 50
		self.h = 50

	def update(self):
		return True

	def Collided(self):
		pass

class Pot(Sprite):
	def __init__(self,locationx, locationy):
		super().__init__(locationx, locationy)
		self.maxImageNum = 2
		self.animationNum = 0
		self.inOnePiece = True
		self.xDirection = 0
		self.yDirection = 0
		self.moveUp = False
		self.moveRight = False
		self.moveDown = False
		self.moveLeft = False
		self.countDown = 15
		self.w = 35
		self.h = 35
		self.images = []
		self.loadImage()
		self.image = self.images[0]
		

	def loadImage(self):
		if (len(self.images) == 0):
			for x in range(1,3):
				self.images.append(pygame.image.load("Images/pot"+ str(x) + ".png"))

class Boomerang(Sprite):
	def __init__(self):
		self.x = 10
		self.y = 10
		self.w = 8;
		self.h = 12
		self.speed = 5
		self.isActive = True
		self.animationNum = 0
		self.maxImageNum = 4
		self.images = []
		self.loadImage()
		self.image = self.images[self.animationNum]
		self.xDirection = 0
		self.yDirection = 0

	def loadImage(self):
		if (len(self.images) == 0):
			for x in range(1,self.maxImageNum + 1):
				self.images.append(pygame.image.load("Images/boomerang"+ str(x) + ".png"))

	def cycleImages(self):
		if (self.animationNum == self.maxImageNum - 1):
			self.animationNum = 0
		self.image = self.images[self.animationNum]
		self.animationNum += 1


	def Collided(self):
		self.isActive = False

	def update(self):
		self.x += self.speed * self.xDirection
		self.y += self.speed * self.yDirection
		self.cycleImages()
		return self.isActive

		
		



class Model():
	def __init__(self):
		self.sprites = []
		self.link = Link()
		self.brick1 = Brick(400,400)
		self.Pot1 = Pot(300,300)
		self.sprites.append(self.link)
		self.sprites.append(self.brick1)
		self.sprites.append(self.Pot1)
		

	def update(self):
		for i in self.sprites:
			for j in self.sprites:
				if i != j:
					self.collide = self.isThereACollision(i, j)
					if (self.collide):
						if isinstance(i,Link) and not isinstance(j,Boomerang):
							self.link.getOutOfSprite(j)


			i.update()

	def addBoomerang(self):
		self.boom = Boomerang()
		if (self.link.getDirection() == 1):
			self.boom.xDirection = 0
			self.boom.yDirection = -1
			self.boom.x = self.link.x + (self.link.w * 1/2)
			self.boom.y = self.link.y
		elif (self.link.getDirection() == 2):
			self.boom.xDirection = 1
			self.boom.yDirection = 0
			self.boom.x = self.link.x + self.link.w
			self.boom.y = self.link.y + (self.link.h * 1/2)
		elif (self.link.getDirection() == 3):
			self.boom.xDirection = 0
			self.boom.yDirection = 1
			self.boom.x = self.link.x + (self.link.w * 1/2)
			self.boom.y = self.link.y + self.link.h
		elif (self.link.getDirection() == 4):
			self.boom.xdirection = -1
			self.boom.ydirection = 0
			self.boom.x = self.link.x
			self.boom.y = self.link.y + (self.link.h * 1/2)
		self.sprites.append(self.boom)
	
	def isThereACollision(self, l, b):
		if (l.x + l.w < b.x):
			return False;
		
		if (l.x > b.x + b.w):
			return False;
		
		if(l.y + l.h < b.y):
			return False;
		
		if (l.y > b.y + b.h):
			return False;
		return True;
		

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
			elif event.type == KEYUP:
				if event.key == K_LCTRL:
					self.model.addBoomerang()
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