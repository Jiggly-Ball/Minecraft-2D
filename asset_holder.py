import pygame as pg
from data import Data

def load_image(name:str):
	image_load = pg.image.load(f"assets\{name}").convert()
	final_image = pg.transform.scale(image_load, (Data.block_size, Data.block_size))
	return final_image

class player:
	pos = {"x":Data.block_size*5, "y":Data.block_size*3}
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