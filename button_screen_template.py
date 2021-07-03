import pygame
import subprocess
import logging
import json

log_format = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(filename = 'Interface Log.Log',
					level = logging.DEBUG,
					format = log_format,
					filemode = 'w')

logger = logging.getLogger()

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

def loadButtonDict(name, names):
	with open(name + '_points.txt', 'r') as f:
		points = eval(f.read())

	buttons = makeButtonDict(names, points)

	return buttons

class Action(object):
	def __init__(self, keyword):
		self.keyword = keyword

class InterfaceAction(Action):
	def __init__(self, keyword, **kwargs):
		Action.__init__(self, keyword)
		self.image = kwargs['image']
		self.buttons = kwargs['buttons']

	def run(self, screen):
		screen.image = self.image
		screen.buttons = self.buttons

class CmdAction(Action):
	def __init__(self, keyword, cmd):
		Action.__init__(self, keyword)
		self.cmd_list = cmd.split()

	def run(self, *args):
		subprocess.run(self.cmd_list)

class ActionHandler(object):
	def __init__(self, *actions):
		self.actions = actions
	def update(self, keyword, screen):
		for action in self.actions:
			if action.keyword == keyword:
				action.run(screen)
				logger.info(f'"{keyword}" action has been run.')


class Interface(object):
	def __init__(self, img, name, fps = 60, 
								  mult = 1, 
								  mode = 'debug-points',
								  frame = True):
		pygame.init()
		logger.info('Pygame initalized.')
		self.screen = Screen(img, name, mode, fps, mult, frame)
		logger.info('Screen Initalized.')
class Screen(object):
	def __init__(self, img, name, mode,
								  fps, 
								  mult,
								  frame):

		''' First, we're gonna set up the variables, then
		we'll actually make the window ready for the 
		mainloop
		'''

		self.name, self.fps, self.mult = name, fps, mult
		
		self.img = pygame.image.load(img)
		self.width, self.height = self.img.get_size()
		self.width, self.height = self.width*self.mult, self.height*self.mult
		logger.info(f'Window Width: {self.width}')
		logger.info(f'Window Height: {self.height}')

		self.alive = True

		self.mode = mode
		logger.info(f'Mode: {self.mode}')
		if self.mode == 'debug-points':
			self.points = []
			self.set = []
			self.ready = False
			self.click_released = False
		elif self.mode == 'debug-hitboxes':
			self.buttons = []
		else:
			self.ready = False
			self.click_released = False
			self.action = None
			self.actions = []

		''' Possible Modes:
		- debug-points
		- debug-hitboxes
		- live
		'''

		if frame:
			self.screen = pygame.display.set_mode((self.width, self.height))
		else:
			self.screen = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)
		
		pygame.display.set_caption(self.name)
		self.clock = pygame.time.Clock()

	def loadButtonDict(self, names):
		with open(self.name + '_points.txt', 'r') as f:
			points = eval(f.read())

		self.buttons = makeButtonDict(names, points)

	def addActions(self, *args):
		for action in args:
			self.actions.append(action)

	def loop(self):
		if self.mode == 'debug-points':
			self.pointLoop()
		elif self.mode == 'debug-hitboxes':
			self.hitboxLoop()
		else:
			self.liveLoop()

	def pointLoop(self):

		# fps 
		self.clock.tick(self.fps)

		# input 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.alive = False

		clicks = pygame.mouse.get_pressed()
		mouse_pos = pygame.mouse.get_pos()

		# update 
		if clicks[0] and not self.ready:
			self.ready = True

		if not clicks[0] and self.ready:
			self.click_released = True
			
		if self.click_released:
			self.click_released = False
			self.ready = False
			self.set.append(mouse_pos)

			if len(self.set) == 2: # if set is full
				self.points.append(self.set)
				self.set = []

		# render 
		self.screen.blit(pygame.transform.scale(self.img, (self.width, self.height)), (0,0))
		pygame.display.flip()

	def hitboxLoop(self):
		''' This loop will create the window and display the hitboxes for each button.
		However, there is no interaction with the buttons. To get that, you have to
		set the mode of the interface to live.
		'''

		# fps 
		self.clock.tick(self.fps)

		# input 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.alive = False

		# render 
		self.screen.blit(pygame.transform.scale(self.img, (self.width, self.height)), (0,0))

		for rect in self.buttons.values():
			pygame.draw.rect(self.screen, (0,0,0, 100), rect)

		pygame.display.flip()

	def liveLoop(self):
		''' This loop will create the window and allow for interaction between the 
		buttons and actions.
		'''

		# reset actions
		self.action = None

		# fps 
		self.clock.tick(self.fps)

		# input 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.alive = False

		clicks = pygame.mouse.get_pressed()
		mouse_pos = pygame.mouse.get_pos()

		# update 
		if clicks[0] and not self.ready:
			self.ready = True

		if not clicks[0] and self.ready:
			self.click_released = True
			
		if self.click_released:
			self.click_released = False
			self.ready = False
			for name, rect in self.buttons.items():
				if rect.collidepoint(mouse_pos):
					self.action = name

		self.checkActions()

		# render 
		self.screen.blit(pygame.transform.scale(self.img, (self.width, self.height)), (0,0))

		pygame.display.flip()
	def checkActions(self):
		if 'start' == self.action:
			print('triggered')
		for action_tuple in self.actions:
			kw, img, button_dict = action_tuple
			if kw == self.action:
				print('triggered')
				self.img = pygame.image.load(img)
				self.buttons = button_dict
				self.action = None

	def death(self, names):
		if self.mode == 'debug-points':
			with open(self.name + '_points.txt', 'w') as f:
				f.write(str(self.points))


if __name__ == '__main__':
	test = Interface('start.png', 'start', mult = 50, mode = 'live')
	names = ['end']
	test.screen.loadButtonDict(names)
	end_action = ('end', 'end.png', loadButtonDict('end', ['start']))
	start_action = ('start', 'start.png', loadButtonDict('start', ['end']))
	test.screen.addActions(end_action, start_action)
	while test.screen.alive:
		test.screen.loop()
	test.screen.death(names)