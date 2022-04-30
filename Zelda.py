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
		self.speed = 8

	def update(self):
		pass
	def loadImage(self):
		pass
	def Collided(self):
		pass


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

	def cycleImages(self):
		if(self.inOnePiece):
			self.animationNum = self.maxImageNum - self.maxImageNum
		else:
			self.animationNum = self.maxImageNum - 1
		self.image = self.images[self.animationNum]


	def Collided(self):
		self.inOnePiece = False
		self.speed = 0

	# Pot movement
	def movePotUp(self):
		self.xDirection = 0
		self.yDirection = -1
		self.y += self.speed * self.yDirection
    
	def movePotRight(self):
		self.xDirection = 1
		self.yDirection = 0
		self.x += self.speed * self.xDirection
        
    
	def movePotDown(self):
		self.xDirection = 0
		self.yDirection = 1
		self.y += self.speed * self.yDirection
    
	def movePotLeft(self):
		self.xDirection = -1
		self.yDirection = 0
		self.x += self.speed * self.xDirection

	def setMoveDown(self,i):
		self.moveDown = i
    

	def update(self):
		if (self.moveUp):
			self.movePotUp()
		if (self.moveRight):
			self.movePotRight()
		if (self.moveDown):
			self.movePotDown()
		if (self.moveLeft):
			self.movePotLeft()
		self.cycleImages()
		if not(self.inOnePiece):
			self.countDown -= 1
			if (self.countDown == 0):
				self.isActive = False
		return self.isActive
		

class Boomerang(Sprite):
	def __init__(self):
		self.x = 10
		self.y = 10
		self.w = 8
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
		self.sprites.append(Brick(0,0))
		self.sprites.append(Brick(0,50))
		self.sprites.append( Brick(0,100))
		self.sprites.append( Brick(0,150))
		self.sprites.append( Brick(0,200))
		self.sprites.append( Brick(0,250))
		self.sprites.append( Brick(0,300))
		self.sprites.append( Brick(0,350))
		self.sprites.append( Brick(0,400))
		self.sprites.append( Brick(0,450))
		self.sprites.append( Brick(50,450))
		self.sprites.append( Brick(0,450))
		self.sprites.append( Brick(50,450))
		self.sprites.append( Brick(100,450))
		self.sprites.append( Brick(100,400))
		self.sprites.append( Brick(0,450))
		self.sprites.append( Brick(350,350))
		self.sprites.append( Brick(350,400))
		self.sprites.append( Brick(400,400))
		self.sprites.append( Brick(400,350))
		self.sprites.append( Brick(450,350))
		self.sprites.append( Brick(450,400))
		self.sprites.append( Brick(600,400))
		self.sprites.append( Brick(600,350))
		self.sprites.append( Brick(650,350))
		self.sprites.append( Brick(650,150))
		self.sprites.append( Brick(650,100))
		self.sprites.append( Brick(650,50))
		self.sprites.append( Brick(650,0))
		self.sprites.append( Brick(700,0))
		self.sprites.append( Brick(700,50))
		self.sprites.append( Brick(700,450))
		self.sprites.append( Brick(700,400))
		self.sprites.append( Brick(700,100))
		self.sprites.append( Brick(700,150))
		self.sprites.append( Brick(750,0))
		self.sprites.append( Brick(800,0))
		self.sprites.append( Brick(850,0))
		self.sprites.append( Brick(900,0))
		self.sprites.append( Brick(1000,0))
		self.sprites.append( Brick(950,0))
		self.sprites.append( Brick(1050,0))
		self.sprites.append( Brick(1100,0))
		self.sprites.append( Brick(1150,0))
		self.sprites.append( Brick(1200,0))
		self.sprites.append( Brick(1300,0))
		self.sprites.append( Brick(1250,0))
		self.sprites.append( Brick(1350,0))
		self.sprites.append( Brick(1350,50))
		self.sprites.append( Brick(1350,100))
		self.sprites.append( Brick(1350,200))
		self.sprites.append( Brick(1350,150))
		self.sprites.append( Brick(1350,250))
		self.sprites.append( Brick(1350,300))
		self.sprites.append( Brick(1350,400))
		self.sprites.append( Brick(1350,350))
		self.sprites.append( Brick(1350,450))
		self.sprites.append( Brick(1300,450))
		self.sprites.append( Brick(1250,450))
		self.sprites.append( Brick(1150,450))
		self.sprites.append( Brick(1100,450))
		self.sprites.append( Brick(1050,450))
		self.sprites.append( Brick(1000,450))
		self.sprites.append( Brick(950,450))
		self.sprites.append( Brick(950,400))
		self.sprites.append( Brick(1000,250))
		self.sprites.append( Brick(1050,250))
		self.sprites.append( Brick(700,500))
		self.sprites.append( Brick(700,550))
		self.sprites.append( Brick(700,600))
		self.sprites.append( Brick(700,650))
		self.sprites.append( Brick(700,700))
		self.sprites.append( Brick(700,750))
		self.sprites.append( Brick(700,950))
		self.sprites.append( Brick(750,950))
		self.sprites.append( Brick(850,700))
		self.sprites.append( Brick(950,700))
		self.sprites.append( Brick(900,700))
		self.sprites.append( Brick(1000,700))
		self.sprites.append( Brick(1050,700))
		self.sprites.append( Brick(1100,700))
		self.sprites.append( Brick(1150,700))
		self.sprites.append( Brick(1200,950))
		self.sprites.append( Brick(1150,950))
		self.sprites.append( Brick(1100,950))
		self.sprites.append( Brick(1050,950))
		self.sprites.append( Brick(950,950))
		self.sprites.append( Brick(1000,950))
		self.sprites.append( Brick(850,950))
		self.sprites.append( Brick(800,950))
		self.sprites.append( Brick(900,950))
		self.sprites.append( Brick(1250,950))
		self.sprites.append( Brick(1300,950))
		self.sprites.append( Brick(1350,950))
		self.sprites.append( Brick(1350,900))
		self.sprites.append( Brick(1350,850))
		self.sprites.append( Brick(1350,800))
		self.sprites.append( Brick(1350,650))
		self.sprites.append( Brick(1350,700))
		self.sprites.append( Brick(1350,600))
		self.sprites.append( Brick(1350,550))
		self.sprites.append( Brick(1350,500))
		self.sprites.append( Brick(1300,500))
		self.sprites.append( Brick(0,950))
		self.sprites.append( Brick(0,850))
		self.sprites.append( Brick(0,900))
		self.sprites.append( Brick(0,800))
		self.sprites.append( Brick(0,750))
		self.sprites.append( Brick(0,700))
		self.sprites.append( Brick(0,650))
		self.sprites.append( Brick(0,600))
		self.sprites.append( Brick(0,550))
		self.sprites.append( Brick(50,950))
		self.sprites.append( Brick(150,950))
		self.sprites.append( Brick(200,950))
		self.sprites.append( Brick(250,950))
		self.sprites.append( Brick(400,950))
		self.sprites.append( Brick(350,950))
		self.sprites.append( Brick(450,950))
		self.sprites.append( Brick(550,950))
		self.sprites.append( Brick(600,950))
		self.sprites.append( Brick(650,750))
		self.sprites.append( Brick(650,650))
		self.sprites.append( Brick(650,700))
		self.sprites.append( Brick(650,600))
		self.sprites.append( Brick(650,500))
		self.sprites.append( Brick(650,550))
		self.sprites.append( Brick(0,500))
		self.sprites.append( Brick(450,600))
		self.sprites.append( Brick(150,700))
		self.sprites.append( Brick(200,750))
		self.sprites.append( Brick(250,800))
		self.sprites.append( Brick(300,800))
		self.sprites.append( Brick(400,800))
		self.sprites.append( Brick(350,800))
		self.sprites.append( Brick(450,800))
		self.sprites.append( Brick(350,450))
		self.sprites.append( Brick(400,450))
		self.sprites.append( Brick(450,450))
		self.sprites.append( Brick(600,450))
		self.sprites.append( Brick(650,450))
		self.sprites.append( Brick(50,0))
		self.sprites.append( Brick(100,0))
		self.sprites.append( Brick(150,0))
		self.sprites.append( Brick(200,0))
		self.sprites.append( Brick(250,0))
		self.sprites.append( Brick(300,0))
		self.sprites.append( Brick(350,0))
		self.sprites.append( Brick(400,0))
		self.sprites.append( Brick(450,0))
		self.sprites.append( Brick(500,0))
		self.sprites.append( Brick(550,0))
		self.sprites.append( Brick(600,0))
		self.sprites.append( Brick(150,350))
		self.sprites.append( Brick(200,350))
		self.sprites.append( Brick(150,400))
		self.sprites.append( Brick(200,400))
		self.sprites.append( Brick(150,450))
		self.sprites.append( Brick(200,450))
		self.sprites.append( Brick(250,300))
		self.sprites.append( Brick(300,300))
		self.sprites.append( Brick(50,500))
		self.sprites.append( Brick(150,500))
		self.sprites.append( Brick(100,500))
		self.sprites.append( Brick(200,500))
		self.sprites.append( Brick(300,500))
		self.sprites.append( Brick(250,500))
		self.sprites.append( Brick(350,500))
		self.sprites.append( Brick(400,500))
		self.sprites.append( Brick(450,500))
		self.sprites.append( Brick(600,500))
		self.sprites.append( Brick(100,950))
		self.sprites.append( Brick(300,950))
		self.sprites.append( Brick(500,950))
		self.sprites.append( Brick(650,950))
		self.sprites.append( Brick(1250,500))
		self.sprites.append( Brick(1200,500))
		self.sprites.append( Brick(1150,500))
		self.sprites.append( Brick(1100,500))
		self.sprites.append( Brick(1000,500))
		self.sprites.append( Brick(1050,500))
		self.sprites.append( Brick(950,500))
		self.sprites.append( Brick(850,400))
		self.sprites.append( Brick(850,450))
		self.sprites.append( Brick(900,500))
		self.sprites.append( Brick(850,500))
		self.sprites.append( Brick(700,350))
		self.sprites.append( Brick(1200,450))
		self.sprites.append( Brick(1100,400))
		self.sprites.append( Brick(1100,350))
		self.sprites.append( Brick(1100,300))
		self.sprites.append( Brick(1300,400))
		self.sprites.append( Brick(1300,350))
		self.sprites.append( Brick(1300,50))
		self.sprites.append( Brick(1300,100))
		self.sprites.append( Brick(1300,1500))
		self.sprites.append( Brick(1250,100))
		self.sprites.append( Brick(1250,50))
		self.sprites.append( Brick(750,50))
		self.sprites.append( Brick(800,50))
		self.sprites.append( Brick(750,100))
		self.sprites.append( Brick(1300,550))
		self.sprites.append( Brick(1250,550))
		self.sprites.append( Brick(1300,600))
		self.sprites.append( Brick(1300,900))
		self.sprites.append( Brick(1200,900))
		self.sprites.append( Brick(1250,900))
		self.sprites.append( Brick(1250,850))
		self.sprites.append( Brick(1300,850))
		self.sprites.append( Brick(1350,750))
		self.sprites.append( Brick(1300,800))
		self.sprites.append( Pot(600,200))
		self.sprites.append( Pot(600,250))
		self.sprites.append( Pot(600,300))
		self.sprites.append( Pot(300,750))
		self.sprites.append( Pot(350,750))
		self.sprites.append( Pot(300,900))
		self.sprites.append( Pot(350,900))
		self.sprites.append( Pot(400,900))
		self.sprites.append( Pot(1050,650))
		self.sprites.append( Pot(1100,650))
		self.sprites.append( Pot(1150,650))
		self.sprites.append( Pot(1200,850))
		self.sprites.append( Pot(1250,800))
		self.sprites.append( Pot(1300,750))
		self.sprites.append( Pot(1300,700))
		self.sprites.append( Pot(1150,900))
		self.sprites.append( Pot(850,650))
		self.sprites.append( Pot(950,350))
		self.sprites.append( Pot(1000,200))
		self.sprites.append( Pot(1050,200))
		self.sprites.append( Pot(1200,400))
		self.sprites.append( Pot(1300,300))
		

	def update(self):
		for i in self.sprites:
			for j in self.sprites:
				if i != j:
					self.collide = self.isThereACollision(i, j)
					if (self.collide):
						if isinstance(i,Link) and not isinstance(j,Boomerang):
							i.getOutOfSprite(j)
						if isinstance(i,Boomerang) and not isinstance(j,Link):
							i.Collided()
						if isinstance(i,Pot) and not isinstance(j,Link):
							i.Collided()
						elif isinstance(i,Link) and isinstance(j, Pot):
							if (i.getDirection() == 1):
								j.moveUp = True
								j.moveRight = False
								j.moveDown = False
								j.moveLeft = False
							elif (i.getDirection() == 2):
								j.moveUp = False
								j.moveRight = True
								j.moveDown = False
								j.moveLeft = False
							elif (i.getDirection() == 3):
								j.moveUp = False
								j.moveRight = False
								j.moveDown = True
								j.moveLeft = False
							elif (i.getDirection() == 4):
								j.moveUp = False
								j.moveRight = False
								j.moveDown = False
								j.moveLeft = True
						


			i.update()
			if (i.update() == False):
				self.sprites.remove(i)

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
			self.boom.xDirection = -1
			self.boom.yDirection = 0
			self.boom.x = self.link.x
			self.boom.y = self.link.y + (self.link.h * 1/2)
		self.sprites.append(self.boom)
	
	def isThereACollision(self, l, b):
		if (l.x + l.w < b.x):
			return False
		
		if (l.x > b.x + b.w):
			return False
		
		if(l.y + l.h < b.y):
			return False
		
		if (l.y > b.y + b.h):
			return False
		return True
		

class View():
	windowXSize = 700;
	windowYSize = 500;
	scrollPositonX = 0;
	scrollPositonY = 0;
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
			self.screen.blit(sprite.image, (sprite.x - View.scrollPositonX,sprite.y - View.scrollPositonY))
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
			self.viewDecreaseX()
		if keys[K_RIGHT]:
			self.model.link.moveRight()
			self.viewIncreaseX()
			self.viewIncreaseX
		if keys[K_UP]:
			self.model.link.moveUp()
			self.viewDecreaseY()
		if keys[K_DOWN]:
			self.model.link.moveDown()
			self.viewIncraseY()
	
	def viewIncreaseX(self):
		if (self.model.link.x == View.windowXSize):
			View.scrollPositonX += View.windowXSize;
		
	
	def viewDecreaseX(self):
		if (self.model.link.x == View.windowXSize):
			View.scrollPositonX -= View.windowXSize;
		

	
	def viewIncraseY(self):
		if (self.model.link.y == View.windowYSize):
			View.scrollPositonY += View.windowYSize;
		
	
	def viewDecreaseY(self):
		if (self.model.link.y == View.windowYSize):
			View.scrollPositonY -= View.windowYSize;
		
	




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