import pygame
from settings import *
from sys import exit
from pytmx.util_pygame import load_pygame
from os.path import join

from sprites import Sprite, AnimatedSprite, BorderSprite, ColidableSprite, TrasitionSprite
from entities import Player
from groups import AllSprites

from support import *
from game_data import *
from monster import Monster
from monster_index import MonsterIndex
from battle import Battle

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('SchoolRPG')
        self.clock = pygame.time.Clock()

        # player and fairy
        self.player_monsters = {
            0: Monster('Player', 30),
            1: Monster('Plumette', 30),
            2: Monster('Finsta', 30),
        }

        self.dummy_monsters = {
            0: Monster('Plumette', 30),
            1: Monster('Finsta', 30),
            2: Monster('Pouch', 30),
            3: Monster('Draem', 30),
            4: Monster('Atrox', 30),
            5: Monster('Charmadillo', 30),
        }

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.colidable_sprites = pygame.sprite.Group()
        self.transition_sprites = pygame.sprite.Group()
        self.monster_sprites = pygame.sprite.Group()

        # transition / tint
        self.transition_target = None
        self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_mode = 'untint'
        self.tint_progress = 0
        self.tint_direction = -1
        self.tint_speed = 600

        # colidable lessons
        self.colidable_target = None

        self.import_assets()
        self.setup(self.tmx_maps['world'], 'autumn_first_lesson')

        # overlays
        self.monster_index = MonsterIndex(self.player_monsters, self.fonts, self.monster_frames)
        self.index_open = False
        self.battle = None

    def import_assets(self):
        self.tmx_maps = {
            'world': load_pygame('data/tmx/world.tmx'),
            'home': load_pygame('data/tmx/home.tmx'),
        }

        self.monster_frames = {
            'icons': import_folder_dict('graphics/icons'),
            'monsters': import_folder_dict('graphics/monsters')
        }

        self.overworld_frames = {
            'water': import_folder('graphics/tilesets/water'),
            'coast': coast_importer(24, 12, 'graphics/tilesets/coast'),
            'characters': all_character_import('graphics/characters'),
        }
        # font
        self.fonts = {
            'title': pygame.font.Font('data/fonts/TeletactileRus.ttf', 32),
            'text': pygame.font.Font('data/fonts/TeletactileRus.ttf', 24),
            'regular': pygame.font.Font('data/fonts/TeletactileRus.ttf', 18),
            'small': pygame.font.Font('data/fonts/TeletactileRus.ttf', 14)
        }
        self.bg_frames = import_folder_dict('graphics/backgrounds')


    def setup(self, tmx_map, player_start_pos):
        # clear the map
        for group in (self.all_sprites, self.collision_sprites, self.transition_sprites, self.colidable_sprites):
            group.empty()

        if tmx_map == self.tmx_maps['world']:
            # collision objects
            for obj in tmx_map.get_layer_by_name('terrain_collisions'):
                BorderSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)),
                             self.collision_sprites)
            for obj in tmx_map.get_layer_by_name('tests_collisions'):
                BorderSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)),
                             self.collision_sprites)
            for obj in tmx_map.get_layer_by_name('lessons_collisions'):
                ColidableSprite((obj.x, obj.y), (obj.width, obj.height), (obj.properties['number'], obj.properties['pos'],
                                                                          obj.properties['target']),
                                self.colidable_sprites)


            # terrain
            for x, y, surf in tmx_map.get_layer_by_name('floor').tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, WORLD_LAYERS['bg'])

            # water
            for obj in tmx_map.get_layer_by_name('water'):
                for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
                    for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
                        AnimatedSprite((x, y), self.overworld_frames['water'], self.all_sprites, WORLD_LAYERS['bg'])

            # coast
            for obj in tmx_map.get_layer_by_name('coast'):
                terrain = obj.properties['terrain']
                side = obj.properties['side']
                AnimatedSprite((obj.x, obj.y), self.overworld_frames['coast'][terrain][side], self.all_sprites,
                               WORLD_LAYERS['bg'])

            # objects
            for obj in tmx_map.get_layer_by_name('terrain_objects'):
                if obj.name == 'top':
                    Sprite((obj.x, obj.y), obj.image, self.all_sprites, WORLD_LAYERS['top'])
                else:
                    Sprite((obj.x, obj.y), obj.image, self.all_sprites)

            # transition objects
            for obj in tmx_map.get_layer_by_name('transition'):
                TrasitionSprite((obj.x, obj.y), (obj.width, obj.height), (obj.properties['target'], obj.properties['pos']),
                                self.transition_sprites)

            # school_stuff
            for obj in tmx_map.get_layer_by_name('lessons'):
                Sprite((obj.x, obj.y), obj.image, self.all_sprites, WORLD_LAYERS['bg'])
            for obj in tmx_map.get_layer_by_name('tests'):
                Sprite((obj.x, obj.y), obj.image, self.all_sprites, WORLD_LAYERS['main'])

            # entities
            for obj in tmx_map.get_layer_by_name('entities'):
                if obj.name == 'player' and obj.properties['pos'] == 'autumn_first_lesson':
                    self.player = Player(pos=(obj.x, obj.y),
                                         frames=self.overworld_frames['characters']['player'],
                                         groups=self.all_sprites,
                                         collision_sprites=self.collision_sprites,
                                         colidable_sprites=self.colidable_sprites)

            for obj in tmx_map.get_layer_by_name('home'):
                Sprite((obj.x, obj.y), obj.image, self.all_sprites, WORLD_LAYERS['main'])

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
                                         groups=self.all_sprites,
                                         collision_sprites=self.collision_sprites,
                                         colidable_sprites=self.colidable_sprites)

            for obj in tmx_map.get_layer_by_name('furniture_obj'):
                Sprite((obj.x, obj.y), obj.image, self.all_sprites, WORLD_LAYERS['main'])

            # collisions and transitions
            for obj in tmx_map.get_layer_by_name('collisions'):
                BorderSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)),
                             self.collision_sprites)
            for obj in tmx_map.get_layer_by_name('transitions'):
                TrasitionSprite((obj.x, obj.y), (obj.width, obj.height), (obj.properties['target'], obj.properties['pos']),
                                self.transition_sprites)

    # input
    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_RETURN]:
            self.index_open = not self.index_open
            self.player.blocked = not self.player.blocked


    # transition check
    def transition_check(self):
        sprites = [sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox)]
        if sprites:
            self.transition_target = sprites[0].target
            self.tint_mode = ('tint')

    def tint_screen(self, dt):
        if self.tint_mode == 'untint':
            self.tint_progress -= self.tint_speed * dt
        if self.tint_mode == 'tint':
            self.tint_progress += self.tint_speed * dt
            if self.tint_progress >= 255:
                self.setup(self.tmx_maps[self.transition_target[0]], self.transition_target[1])
                self.tint_mode = 'untint'
                self.transition_target = None

        self.tint_progress = max(0, min(self.tint_progress, 255))
        self.tint_surf.set_alpha(self.tint_progress)
        self.display_surface.blit(self.tint_surf, (0, 0))

    def collide_check(self):
        sprites = [sprite for sprite in self.colidable_sprites if sprite.rect.colliderect(self.player.hitbox)]
        if sprites:
            self.colidable_target = sprites[0].target
            self.collide_window(self.colidable_target)

    def collide_window(self, colidable_target):
        # title
        self.colidable_target = colidable_target
        self.big_text_surf = self.fonts['title'].render(f'Урок {self.colidable_target[0]}: {LESSONS_INFO[self.colidable_target[0]]}', False,
                                             'White')
        self.big_text_rect = self.big_text_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 5))
        pygame.draw.rect(self.display_surface, 'black', self.big_text_rect)
        self.display_surface.blit(self.big_text_surf, self.big_text_rect)

        # press f to start
        self.small_text_surf = self.fonts['text'].render('Нажмите F чтобы начать', False,
                                             'White')
        self.small_text_rect = self.small_text_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4))
        pygame.draw.rect(self.display_surface, 'black', self.small_text_rect)
        self.display_surface.blit(self.small_text_surf, self.small_text_rect)
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_f]:
            self.battle = Battle(self.player_monsters, self.dummy_monsters, self.monster_frames,
                                 self.bg_frames['forest'], self.fonts)


    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            self.display_surface.fill('black')
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    pygame.quit()
                    exit()
                if event.type == keys[pygame.K_h]:
                    self.isHelp = True

            # game logic
            self.input()
            self.all_sprites.update(dt)
            self.transition_check()

            self.all_sprites.draw(self.player.rect.center)

            # overlays
            self.collide_check()
            if self.index_open: self.monster_index.update(dt)
            if self.battle: self.battle.update(dt)

            self.tint_screen(dt)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()