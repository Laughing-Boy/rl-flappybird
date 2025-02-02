# -*- coding: utf-8 -*-
# @Original: https://github.com/sourabhv/FlappyBirdClone
# @Author: Shubham
# @Date:   2016-05-18 22:14:16
# @Last Modified by:   shubham
# @Last Modified time: 2016-05-25 16:16:03

from itertools import cycle
import random
import sys

import pygame
from pygame.locals import *

# headless
import os
 
os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()
# pygame.display.set_mode((1,1))


REWARD_MAX = 1

def getHitmask(image):
	"""returns a hitmask using an image's alpha."""
	mask = []
	for x in range(image.get_width()):
		mask.append([])
		for y in range(image.get_height()):
			mask[x].append(bool(image.get_at((x,y))[3]))
	return mask

def playerShm(playerShm):
	"""oscillates the value of playerShm['val'] between 8 and -8"""
	if abs(playerShm['val']) == 8:
		playerShm['dir'] *= -1

	if playerShm['dir'] == 1:
		 playerShm['val'] += 1
	else:
		playerShm['val'] -= 1


FPS = 30
SCREENWIDTH  = 288
SCREENHEIGHT = 512
# amount by which base can maximum shift to left
PIPEGAPSIZE  = 240 # gap between upper and lower part of pipe
BASEY        = SCREENHEIGHT * 0.79
# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = (
	# red bird
	# (
	# 	'assets/sprites/redbird-upflap.png',
	# 	'assets/sprites/redbird-midflap.png',
	# 	'assets/sprites/redbird-downflap.png',
	# ),
	# blue bird
	(
		# amount by which base can maximum shift to left
		'assets/sprites/bluebird-upflap.png',
		'assets/sprites/bluebird-midflap.png',
		'assets/sprites/bluebird-downflap.png',
	),
	# # yellow bird
	# (
	# 	'assets/sprites/yellowbird-upflap.png',
	# 	'assets/sprites/yellowbird-midflap.png',
	# 	'assets/sprites/yellowbird-downflap.png',
	# ),
)

# list of backgrounds
BACKGROUNDS_LIST = (
	# 'assets/sprites/background-orange.png',
	'assets/sprites/background-black.png',
	# 'assets/sprites/background-day.png',
	# 'assets/sprites/background-night.png',
)

# list of backgrounds
BACKGROUNDS_BLACK = (
	# 'assets/sprites/background-orange.png',
	'assets/sprites/background-black.png',
	# 'assets/sprites/background-day.png',
	# 'assets/sprites/background-night.png',
)


# list of pipes
PIPES_LIST = (
	'assets/sprites/pipe-green.png',
	# 'assets/sprites/pipe-red.png',
)


# pygame.init()
FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Flappy Bird')

# numbers sprites for score display
IMAGES['numbers'] = (
	pygame.image.load('assets/sprites/0.png').convert_alpha(),
	pygame.image.load('assets/sprites/1.png').convert_alpha(),
	pygame.image.load('assets/sprites/2.png').convert_alpha(),
	pygame.image.load('assets/sprites/3.png').convert_alpha(),
	pygame.image.load('assets/sprites/4.png').convert_alpha(),
	pygame.image.load('assets/sprites/5.png').convert_alpha(),
	pygame.image.load('assets/sprites/6.png').convert_alpha(),
	pygame.image.load('assets/sprites/7.png').convert_alpha(),
	pygame.image.load('assets/sprites/8.png').convert_alpha(),
	pygame.image.load('assets/sprites/9.png').convert_alpha()
)

# game over sprite
IMAGES['gameover'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
# message sprite for welcome screen
IMAGES['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()
# base (ground) sprite
IMAGES['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()

# sounds
if 'win' in sys.platform:
	soundExt = '.wav'
else:
	soundExt = '.ogg'

SOUNDS['die']    = pygame.mixer.Sound('assets/audio/die' + soundExt)
SOUNDS['hit']    = pygame.mixer.Sound('assets/audio/hit' + soundExt)
SOUNDS['point']  = pygame.mixer.Sound('assets/audio/point' + soundExt)
SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
SOUNDS['wing']   = pygame.mixer.Sound('assets/audio/wing' + soundExt)


randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()
IMAGES['backgroundB'] = pygame.image.load(BACKGROUNDS_BLACK[0]).convert()

# select random player sprites
randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
IMAGES['player'] = (
	pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
	pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
	pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
)

# select random pipe sprites
pipeindex = random.randint(0, len(PIPES_LIST) - 1)
IMAGES['pipe'] = (
	pygame.transform.rotate(
		pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), 180),
	pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
)

# hismask for pipes
HITMASKS['pipe'] = (
	getHitmask(IMAGES['pipe'][0]),
	getHitmask(IMAGES['pipe'][1]),
)

# hitmask for player
HITMASKS['player'] = (
	getHitmask(IMAGES['player'][0]),
	getHitmask(IMAGES['player'][1]),
	getHitmask(IMAGES['player'][2]),
)


def loadResources():

	randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
	IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

	# select random player sprites
	randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
	IMAGES['player'] = (
		pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
		pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
		pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
	)

	# select random pipe sprites
	pipeindex = random.randint(0, len(PIPES_LIST) - 1)
	IMAGES['pipe'] = (
		pygame.transform.rotate(
			pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), 180),
		pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
	)

	# hismask for pipes
	HITMASKS['pipe'] = (
		getHitmask(IMAGES['pipe'][0]),
		getHitmask(IMAGES['pipe'][1]),
	)

	# hitmask for player
	HITMASKS['player'] = (
		getHitmask(IMAGES['player'][0]),
		getHitmask(IMAGES['player'][1]),
		getHitmask(IMAGES['player'][2]),
	)


def showWelcomeAnimation():
	"""Shows welcome screen animation of flappy bird"""
	# index of player to blit on screen
	playerIndex = 0
	playerIndexGen = cycle([0, 1, 2, 1])
	# iterator used to change playerIndex after every 5th iteration
	loopIter = 0

	playerx = int(SCREENWIDTH * 0.2)
	playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)

	messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
	messagey = int(SCREENHEIGHT * 0.12)

	basex = 0
	# amount by which base can maximum shift to left
	baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

	# player shm for up-down motion on welcome screen
	playerShmVals = {'val': 0, 'dir': 1}

	while True:
		for event in pygame.event.get():
			# print(event)
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()

			if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
				# make first flap sound and return values for mainGame
				# SOUNDS['wing'].play()
				return {
					'playery': playery + playerShmVals['val'],
					'basex': basex,
					'playerIndexGen': playerIndexGen,
				}

		# print('HEHE')
		# from time import sleep
		# sleep(1)
		# SOUNDS['wing'].play()
		return {
			'playery': playery + playerShmVals['val'],
			'basex': basex,
			'playerIndexGen': playerIndexGen,
		}

		# adjust playery, playerIndex, basex
		if (loopIter + 1) % 5 == 0:
			playerIndex = next(playerIndexGen)
		loopIter = (loopIter + 1) % 30
		basex = -((-basex + 4) % baseShift)
		playerShm(playerShmVals)

		# draw sprites
		SCREEN.blit(IMAGES['background'], (0,0))
		SCREEN.blit(IMAGES['player'][playerIndex],
					(playerx, playery + playerShmVals['val']))
		SCREEN.blit(IMAGES['message'], (messagex, messagey))
		SCREEN.blit(IMAGES['base'], (basex, BASEY))

		pygame.display.update()
		FPSCLOCK.tick(FPS)

movementInfo = showWelcomeAnimation()

def main():
	
	bird = FlappyBird(movementInfo)
	from random import choice
	while True:
		crashInfo = bird.flapOnce(choice([True]+[False]*10))
		if crashInfo: break
	
	print(crashInfo)
	# showGameOverScreen(crashInfo)



class FlappyBird():
	def __init__(self):
		loadResources()
		# movementInfo = showWelcomeAnimation()
		self.score = self.playerIndex = self.loopIter = 0
		self.playerIndexGen = movementInfo['playerIndexGen']
		self.playerx, self.playery = int(SCREENWIDTH * 0.2), movementInfo['playery']

		self.basex = movementInfo['basex']
		self.baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

		# get 2 new pipes to add to upperPipes lowerPipes list
		newPipe1 = getRandomPipe()
		newPipe2 = getRandomPipe()

		# list of upper pipes
		self.upperPipes = [
			{'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
			{'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
		]

		# list of lowerpipe
		self.lowerPipes = [
			{'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
			{'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
		]

		self.pipeVelX = -4

		# player velocity, max velocity, downward accleration, accleration on flap
		self.playerVelY    =  -9   # player's velocity along Y, default same as self.playerFlapped
		self.playerMaxVelY =  100   # max vel along Y, max descend speed
		self.playerMinVelY =  -8   # min vel along Y, max ascend speed
		self.playerAccY    =   1   # players downward accleration
		self.playerFlapAcc =  -9   # players speed on flapping
		self.playerFlapped = False # True when player flaps


	def flapOnce(self, action):

		# loadResources()
		# pygame.event.pump()
		
		terminal = False
		reward = 0.1

		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				print('Quiting...')
				pygame.quit()
				sys.exit()
			# if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
		
		assert sum(action) == 1

		if action[1] == 1:
			# print('Flap-Baby')
			if self.playery > -2 * IMAGES['player'][0].get_height():
				self.playerVelY = self.playerFlapAcc
				self.playerFlapped = True
				# SOUNDS['wing'].play()

		# check for crash here
		crashTest = checkCrash({'x': self.playerx, 'y': self.playery, 'index': self.playerIndex},
							   self.upperPipes, self.lowerPipes)
		if crashTest[0]:
			reward = -REWARD_MAX
			terminal = True
			self.__init__()
			# return image_data, reward, terminal
			# return {
			# 	'y': self.playery,
			# 	'groundCrash': crashTest[1],
			# 	'basex': self.basex,
			# 	'upperPipes': self.upperPipes,
			# 	'lowerPipes': self.lowerPipes,
			# 	'score': self.score,
			# 	'playerVelY': self.playerVelY,
			# }

		# check for self.score
		playerMidPos = self.playerx + IMAGES['player'][0].get_width() / 2
		for pipe in self.upperPipes:
			pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
			if pipeMidPos <= playerMidPos < pipeMidPos + 4:
				self.score += 1
				# SOUNDS['point'].play()
				reward = REWARD_MAX

		# self.playerIndex self.basex change
		if (self.loopIter + 1) % 3 == 0:
			self.playerIndex = next(self.playerIndexGen)
		self.loopIter = (self.loopIter + 1) % 30
		self.basex = -((-self.basex + 100) % self.baseShift)

		# player's movement
		if self.playerVelY < self.playerMaxVelY and not self.playerFlapped:
			self.playerVelY += self.playerAccY
		if self.playerFlapped:
			self.playerFlapped = False
		playerHeight = IMAGES['player'][self.playerIndex].get_height()
		self.playery += min(self.playerVelY, BASEY - self.playery - playerHeight)

		# move pipes to left
		for uPipe, lPipe in zip(self.upperPipes, self.lowerPipes):
			uPipe['x'] += self.pipeVelX
			lPipe['x'] += self.pipeVelX

		# add new pipe when first pipe is about to touch left of screen
		if 0 < self.upperPipes[0]['x'] < 5:
			newPipe = getRandomPipe()
			self.upperPipes.append(newPipe[0])
			self.lowerPipes.append(newPipe[1])

		# remove first pipe if its out of the screen
		if self.upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
			self.upperPipes.pop(0)
			self.lowerPipes.pop(0)

		# draw sprites
		SCREEN.blit(IMAGES['background'], (0,0))

		for uPipe, lPipe in zip(self.upperPipes, self.lowerPipes):
			SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
			SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

		SCREEN.blit(IMAGES['base'], (self.basex, BASEY))
		
		# print self.score so player overlaps the self.score
		SCREEN.blit(IMAGES['player'][self.playerIndex], (self.playerx, self.playery))
		
		# SCREEN.blit(IMAGES['backgroundB'], (0,0))
		# print(pygame.surfarray.array3d(pygame.display.get_surface()).shape)
		image_data = pygame.surfarray.array3d(pygame.display.get_surface())


		# window = pygame.display.set_mode()
		# pygame.image.save(window, "screenshot.jpeg")

		showScore(self.score)
		# print(self.score)
		pygame.display.update()
		FPSCLOCK.tick(FPS)

		return image_data, reward, terminal, self.score
 


def showGameOverScreen(crashInfo):
	"""crashes the player down ans shows gameover image"""
	score = crashInfo['score']
	playerx = SCREENWIDTH * 0.2
	playery = crashInfo['y']
	playerHeight = IMAGES['player'][0].get_height()
	playerVelY = crashInfo['playerVelY']
	playerAccY = 2

	basex = crashInfo['basex']

	upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']

	# play hit and die sounds
	# SOUNDS['hit'].play()
	if not crashInfo['groundCrash']:
		pass
		# SOUNDS['die'].play()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
				if playery + playerHeight >= BASEY - 1:
					return

		# player y shift
		if playery + playerHeight < BASEY - 1:
			playery += min(playerVelY, BASEY - playery - playerHeight)

		# player velocity change
		if playerVelY < 15:
			playerVelY += playerAccY

		# draw sprites
		SCREEN.blit(IMAGES['background'], (0,0))

		for uPipe, lPipe in zip(upperPipes, lowerPipes):
			SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
			SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

		SCREEN.blit(IMAGES['base'], (basex, BASEY))
		showScore(score)
		SCREEN.blit(IMAGES['player'][1], (playerx,playery))

		FPSCLOCK.tick(FPS)
		pygame.display.update()


def getRandomPipe():
	"""returns a randomly generated pipe"""
	# y of gap between upper and lower pipe
	gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
	gapY += int(BASEY * 0.2)
	pipeHeight = IMAGES['pipe'][0].get_height()
	pipeX = SCREENWIDTH + 10

	return [
		{'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
		{'x': pipeX, 'y': gapY + PIPEGAPSIZE}, # lower pipe
	]


def showScore(score):
	"""displays score in center of screen"""
	scoreDigits = [int(x) for x in list(str(score))]
	totalWidth = 0 # total width of all numbers to be printed

	for digit in scoreDigits:
		totalWidth += IMAGES['numbers'][digit].get_width()

	Xoffset = (SCREENWIDTH - totalWidth) / 2

	for digit in scoreDigits:
		SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
		Xoffset += IMAGES['numbers'][digit].get_width()


def checkCrash(player, upperPipes, lowerPipes):
	"""returns True if player collders with base or pipes."""
	pi = player['index']
	player['w'] = IMAGES['player'][0].get_width()
	player['h'] = IMAGES['player'][0].get_height()

	# if player crashes into ground
	if player['y'] + player['h'] >= BASEY - 1:
		return [True, True]
	else:

		playerRect = pygame.Rect(player['x'], player['y'],
					  player['w'], player['h'])
		pipeW = IMAGES['pipe'][0].get_width()
		pipeH = IMAGES['pipe'][0].get_height()

		for uPipe, lPipe in zip(upperPipes, lowerPipes):
			# upper and lower pipe rects
			uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
			lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

			# player and upper/lower pipe hitmasks
			pHitMask = HITMASKS['player'][pi]
			uHitmask = HITMASKS['pipe'][0]
			lHitmask = HITMASKS['pipe'][1]

			# if bird collided with upipe or lpipe
			uCollide = pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
			lCollide = pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

			if uCollide or lCollide:
				return [True, False]

	return [False, False]

def pixelCollision(rect1, rect2, hitmask1, hitmask2):
	"""Checks if two objects collide and not just their rects"""
	rect = rect1.clip(rect2)

	if rect.width == 0 or rect.height == 0:
		return False

	x1, y1 = rect.x - rect1.x, rect.y - rect1.y
	x2, y2 = rect.x - rect2.x, rect.y - rect2.y

	for x in range(rect.width):
		for y in range(rect.height):
			if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
				return True
	return False

if __name__ == '__main__':
	main()


