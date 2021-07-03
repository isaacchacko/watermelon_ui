# imports
import pygame
import random
import subprocess
import os
import sys

WARP_PATH = 'C:\\Users\\isaac\\Pictures\\pixel art\\the spaceman' # set to the spaceman so it actually opens the pixel art folder

def openEXE(path):
	subprocess.Popen(path,  stderr=subprocess.PIPE)

def makeRect(pointA, pointB):
	x, y = pointA
	bx, by = pointB
	width = bx - x
	height = by - y
	return x, y, width, height

def makeButton(button_dict, name, pointA, pointB):
	x, y, width, height = makeRect(pointA, pointB)
	button_dict[name] = pygame.Rect(x, y, width, height)

def makeButtonDict(names, points):
	button_dict = {}
	for i, point_set in enumerate(points):
		makeButton(button_dict, names[i], point_set[0], point_set[1])

	return button_dict

# settings
background_img = pygame.image.load('melon_ui.png')
WIDTH, HEIGHT = background_img.get_size()
MULT = 10
WIDTH, HEIGHT = WIDTH * MULT, HEIGHT * MULT
GAME_NAME = 'Watermelon Inc.'
FPS = 60
BLACK = (0,0,0)

# initalization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_NAME)
clock = pygame.time.Clock()
sets = []
ready = False
click_released = False
section = []

button_names = ['warp', 'warp2', 'firefox','cmd','sublime','paint','lol','exit']
points = [[(140, 291), (253, 496)],
		 [(84, 495), (295, 612)], 
		 [(349, 311), (598, 582)],
		 [(641, 301), (895, 596)],
		 [(71, 621), (322, 888)],
		 [(391, 596), (585, 841)],
		 [(654, 602), (919, 907)],
		 [(954, 459), (1129, 709)]]

buttons = makeButtonDict(button_names, points)

# game loop 
running = True
while running:

	action = None

	# fps 
	clock.tick(FPS)

	# input 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	clicks = pygame.mouse.get_pressed()
	mouse_pos = pygame.mouse.get_pos()

	# update 
	if clicks[0] and not ready:
		ready = True

	if not clicks[0] and ready:
		click_released = True
		
	if click_released:
		click_released = False
		ready = False
		for name, rect in buttons.items():
			if rect.collidepoint(mouse_pos):
				action = name


	if action != None:

		# ['warp','firefox','cmd','sublime','paint','lol','exit']

		if action == 'sublime':
			openEXE(r'C:\Program Files\Sublime Text 3\sublime_text.exe')
		if action == 'firefox':
			openEXE(r"C:\Program Files\Mozilla Firefox\firefox.exe") # gag
		if action == 'warp' or action == 'warp2':
			subprocess.Popen(f'explorer /select,"{WARP_PATH}"')
		if action == 'cmd':
			os.system('start cmd')
		if action == 'paint':
			openEXE(r'C:\WINDOWS\system32\mspaint.exe')
		if action == 'lol':
			openEXE(r'"C:\Riot Games\Riot Client\RiotClientServices.exe" --launch-product=league_of_legends --launch-patchline=live')
		if action == 'exit':
			running = False

	# render 
	screen.blit(pygame.transform.scale(background_img, (WIDTH, HEIGHT)), (0,0))

	# draw hitboxes
	# for name, rect in buttons.items():
	# 	pygame.draw.rect(screen, BLACK, rect) 

	pygame.display.flip()

pygame.quit()
sys.exit()