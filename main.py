import pygame as pg
import random
from time import sleep

pg.init()

imported = pg.get_init()
if imported is False:
	raise Exception("Failed Importing PyGame")

block_size = 100
pg.display.set_caption("2D Minecraft")
scrnx, scrny = 1200, 700
window = pg.display.set_mode((scrnx, scrny))


def load_image(name:str):
	image_load = pg.image.load(f"assets\{name}").convert()
	final_image = pg.transform.scale(image_load, (block_size, block_size))
	return final_image


class player:
	pos = {"x":block_size*5, "y":block_size*3}
	img = load_image("player.png")

class stone:
	rate = 90
	img = load_image("stone.png")

class diamondore:
	rate = 4
	img = load_image("diamond.png")

class goldore:
	rate = 5
	img = load_image("gold.png")
	
class cobblestone:
	rate = 40
	img = load_image("cobblestone.png")

class empty:
	img = load_image("empty.png")


class Game:
	def __init__(self, size:int, window_:pg.Surface) -> None:

		fps = 60
		clock = pg.time.Clock()
		running = True

		self.window = window_

		self.data = {}
		self.render = 50
		self.blocks = {
			"stone"      : stone.img      ,
			"cobblestone": cobblestone.img,
			"diamondore" : diamondore.img ,
			"goldore"    : goldore.img    ,
			"empty"      : empty.img
		}
		self.display = []
		self.block_list = ["stone"] * stone.rate + ["diamondore"] * diamondore.rate + ["goldore"] * goldore.rate + ["cobblestone"] * cobblestone.rate

		self.offset_x = self.offset_y = 0
		self.game_start = False
		self.size = size

		font = pg.font.Font('freesansbold.ttf', 32)
		text = font.render(f"Loading Blocks...", True, (0, 255, 0))
		
		self.window.blit(text, (window_.get_width()//9, window_.get_height()//2))
		self.refresh()

		self.generate_world()
		self.display_update()
		sleep(3)
		self.refresh()

		while running:
			for event in pg.event.get():

				if event.type == pg.KEYDOWN:
					if event.key == pg.K_a or event.key == pg.K_LEFT:
						self.map_update("left")

					elif event.key == pg.K_w or event.key == pg.K_UP:
						self.map_update("up")

					elif event.key == pg.K_d or event.key == pg.K_RIGHT:
						self.map_update("right")

					elif event.key == pg.K_s or event.key == pg.K_DOWN:
						self.map_update("down")

				if event.type == pg.QUIT:
					running = False

			clock.tick(fps)


	def map_update(self, direction:str):

		self.data[f"x{player.pos['x']}y{player.pos['y']}"] = "empty"

		if direction == "up":
			player.pos["y"] -= self.size
			self.offset_y += self.size
				
		elif direction == "right":
			player.pos["x"] += self.size
			self.offset_x -= self.size
			
		elif direction == "down":
			player.pos["y"] += self.size
			self.offset_y -= self.size
			
		elif direction == "left":
			player.pos["x"] -= self.size
			self.offset_x += self.size

		self.generate_world()
		self.display_update()
		self.refresh()


	def refresh(self):
		pg.display.flip()

	
	def generate_world(self):

		for y in range(player.pos["y"]+self.render*self.size, player.pos["y"]-(self.render+1)*self.size, -self.size):
			for x in range(player.pos["x"]-self.render*self.size, player.pos["x"]+(self.render*self.size), self.size):
				point = f"x{x}y{y}"
				self.display.append(point)


	def display_update(self):

		for block in self.display:
			x, y = self.read_axises(block)

			try:
				block_img = self.blocks[self.data[block]]
			except KeyError:
				new_block = self.block_gen()
				self.data[block] = new_block
				block_img = self.blocks[new_block]
				
			self.window.blit(block_img, (x+self.offset_x, y+self.offset_y))
			self.window.blit(player.img, (player.pos["x"] + self.offset_x, player.pos["y"] + self.offset_y))
			
			self.display = []


	def block_gen(self) -> str:
		return random.choice(self.block_list)


	def read_axises(self, coords:str) -> tuple:
		xval = yval = ""
		ycount = False
		
		for x in coords: 	# For counting the X value
			if x == "y":
				break
			if x != "x":
				xval = f"{xval}{x}"

		for y in coords: 	# For counting the Y value
			if ycount:
				yval =f"{yval}{y}"
			if y == "y":
				ycount = True
			
		xval = int(xval.strip())
		yval = int(yval.strip())
		return (xval, yval)

Game(block_size, window)