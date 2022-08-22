import pygame
import numpy as np

TILE_SIZE = 32
WIDTH = 20
HEIGHT = 20

PLAYER_COLOR = (0,0,255)
UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3

FOOD_COLOR = (0,255,0)

class Blob:
	def __init__(self,x = 0,y = 0):
		self.x = x
		self.y = y

	def __eq__(self,other):
		return self.x == other.x and self.y == other.y 
	def render(self,canvas,color):
		pygame.draw.rect(canvas, color, pygame.Rect(self.x * TILE_SIZE,self.y * TILE_SIZE,TILE_SIZE,TILE_SIZE))

	def depos(self,maxX,maxY):
		self.x = np.random.randint(0,maxX)
		self.y = np.random.randint(0,maxY)
class Snake(Blob):
	def __init__(self,x,y):
		Blob.__init__(self,x,y)

		self.next_move = RIGHT

		self.prev_poses = []
		self.size = 1
		self.isDead = False
	def render(self,canvas,color):
		for i in range(self.size - 1):
			pygame.draw.rect(canvas, color, pygame.Rect(self.prev_poses[i][0] * TILE_SIZE,self.prev_poses[i][1] * TILE_SIZE,TILE_SIZE,TILE_SIZE))
		pygame.draw.rect(canvas, color, pygame.Rect(self.x * TILE_SIZE,self.y * TILE_SIZE,TILE_SIZE,TILE_SIZE))
	def input(self,event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT and self.next_move != LEFT:
				self.next_move = RIGHT
			if event.key == pygame.K_LEFT and self.next_move != RIGHT:
				self.next_move = LEFT
			if event.key == pygame.K_UP and self.next_move != DOWN:
				self.next_move = UP
			if event.key == pygame.K_DOWN and self.next_move != UP:
				self.next_move = DOWN

	def handleSize(self,food):
		hitFood = False
		if food.x == self.x and food.y == self.y:
			self.size += 1
			hitFood = True

		self.prev_poses.append((self.x,self.y))
		if len(self.prev_poses) > self.size - 1:
			self.prev_poses.pop(0)

			
		return hitFood
	def collisionWithBody(self):
		for part in self.prev_poses:
			if part[0] == self.x and part[1] == self.y:
				self.isDead = True
				break
	def collideWithFood(self,food):
		for part in self.prev_poses:
			if part.x == food.x and part.y == food.y:
				return True
		return self.x == food.x and self.y == food.y
	def move(self):		
		if self.next_move == RIGHT:
			self.x += 1
		elif self.next_move == LEFT:
			self.x -= 1
		elif self.next_move == UP:
			self.y -= 1
		elif self.next_move == DOWN:
			self.y += 1

		if self.x > WIDTH - 1:
			self.x = 0
		elif self.x < 0:
			self.x = WIDTH - 1
		if self.y > HEIGHT - 1:
			self.y = 0
		elif self.y < 0:
			self.y = HEIGHT - 1

	def update(self,food):
		self.collisionWithBody()
		hitFood = self.handleSize(food)
		self.move()
		return self.isDead , hitFood


class Game:
	def __init__(self):
		self.player = Snake(0, 0)
		self.food = Blob(0, 5)
		self.done = False

		pygame.init()
		self.canvas = pygame.display.set_mode((WIDTH * TILE_SIZE , HEIGHT * TILE_SIZE))
		self.clock = pygame.time.Clock()

	def render(self):
		self.canvas.fill((0,0,0))
		self.food.render(self.canvas,FOOD_COLOR)
		self.player.render(self.canvas,PLAYER_COLOR)
		pygame.display.update()

	def input(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.done = True
			self.player.input(event)


	def update(self):
		while not self.done:
			self.clock.tick(10)
			self.render()
			self.done , hitFood =  self.player.update(self.food)
			self.input()


			if not hitFood:
				continue
			self.food.depos(WIDTH,HEIGHT)
			if self.food == self.player:
				while self.player.collideWithFood(self.food):
					self.food.depos(WIDTH,HEIGHT)
