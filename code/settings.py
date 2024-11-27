import pygame
from pygame.math import Vector2 as vector
from sys import exit

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 64
ANIMATION_SPEED = 6
BATTLE_OUTLINE_WIDTH = 4

WORLD_LAYERS = {
	'water': 0,
	'bg': 1,
	'shadow': 2,
	'main': 3,
	'top': 4
}

BATTLE_POSITIONS = {
	'left': {'top': (360, 260), 'center': (190, 400), 'bottom': (410, 520)},
	'right': {'top': (900, 260), 'center': (1110, 390), 'bottom': (900, 550)}
}

COLORS = {
	'white': '#f4fefa',
	'pure white': '#ffffff',
	'dark': '#2b292c',
	'light': '#c8c8c8',
	'gray': '#3a373b',
	'gold': '#ffd700',
	'light-gray': '#4b484d',
	'fire':'#f8a060',
	'water':'#50b0d8',
	'plant': '#64a990',
	'black': '#000000',
	'red': '#f03131',
	'blue': '#66d7ee',
	'normal': '#ffffff',
	'dark white': '#f0f0f0'
}