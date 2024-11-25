import pygame
from settings import *
from sys import exit
from pytmx.util_pygame import load_pygame
from os.path import join

from sprites import Sprite, AnimatedSprite
from entities import Player
from groups import AllSprites

from support import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('SchoolRPG')
        self.clock = pygame.time.Clock()

        # groups
        self.all_sprites = AllSprites()

        self.import_assets()
        self.setup(self.tmx_maps['world'], 'autumn_first_lesson')

    def import_assets(self):
        self.tmx_maps = {
            'world': load_pygame('data/tmx/world.tmx'),
            'home': load_pygame('data/tmx/home.tmx'),
        }

        self.overworld_frames = {
            'water': import_folder('graphics/tilesets/water'),
            'coast': coast_importer(24, 12, 'graphics/tilesets/coast'),
            'characters': all_character_import('graphics/characters'),
        }


    def setup(self, tmx_map, player_start_pos):
        if tmx_map == self.tmx_maps['world']:
            # terrain
            for x, y, surf in tmx_map.get_layer_by_name('floor').tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

            # water
            for obj in tmx_map.get_layer_by_name('water'):
                for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
                    for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
                        AnimatedSprite((x, y), self.overworld_frames['water'], self.all_sprites)

            # coast
            for obj in tmx_map.get_layer_by_name('coast'):
                terrain = obj.properties['terrain']
                side = obj.properties['side']
                AnimatedSprite((obj.x, obj.y), self.overworld_frames['coast'][terrain][side], self.all_sprites)

            # objects
            for obj in tmx_map.get_layer_by_name('terrain_objects'):
                Sprite((obj.x, obj.y), obj.image, self.all_sprites)

            # school_stuff
            for layers in ['lessons', 'tests']:
                for obj in tmx_map.get_layer_by_name(layers):
                    Sprite((obj.x, obj.y), obj.image, self.all_sprites)

            # entities
            for obj in tmx_map.get_layer_by_name('entities'):
                if obj.name == 'player' and obj.properties['pos'] == 'autumn_first_lesson':
                    self.player = Player(pos=(obj.x, obj.y),
                                         frames=self.overworld_frames['characters']['player'],
                                         groups=self.all_sprites)

        if tmx_map == self.tmx_maps['home']:
            # terrain
            for x, y, surf in tmx_map.get_layer_by_name('floor').tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

            # furniture
            for layers in ['doors_windows', 'furniture']:
                for x, y, surf in tmx_map.get_layer_by_name(layers).tiles():
                    Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

            # player
            for obj in tmx_map.get_layer_by_name('entities'):
                if obj.name == 'player' and obj.properties['pos'] == 'enterance':
                    self.player = Player(pos=(obj.x, obj.y),
                                         frames=self.overworld_frames['characters']['player'],
                                         groups=self.all_sprites)

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    pygame.quit()
                    exit()

            # game logic
            self.all_sprites.update(dt)
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()