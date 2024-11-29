import random
from random import choice

from settings import *
from sprites import MonsterSprite, MonsterLevelSprite, MonsterNameSprite, MonsterStatsSprite, MonsterOutlineSprite, AttackSprite
from groups import BattleSprites
from game_data import ATTACK_DATA
from timer import Timer

import sympy as sp
import pygame

class Battle:
    def __init__(self, player_monsters, opponent_monsters, monster_frames, bg_surf, fonts, end_battle):
        # general
        self.display_surface = pygame.display.get_surface()
        self.bg_surf = bg_surf
        self.monster_frames = monster_frames
        self.fonts = fonts
        self.monster_data = {'player': player_monsters, 'opponent': opponent_monsters}
        self.battle_over = False
        self.end_battle = end_battle

        # timers
        self.timers = {
            'opponent delay': Timer(600, func=self.opponent_attack)
        }

        # groups
        self.battle_sprites = BattleSprites()
        self.player_sprites = pygame.sprite.Group()
        self.opponent_sprites = pygame.sprite.Group()

        # control
        self.current_monster = None
        self.selection_mode = None
        self.selection_side = 'player'
        self.selected_attack = None
        self.indexes = {
            'general': 0,
            'monster': 0,
            'attacks': 0,
            'target': 0,
        }

        # equation
        self.isEquation = False
        self.equation_resolved = False
        self.current_equation = self.generate_linear_equation()
        self.player_answer = ""
        self.current_solution = None

        self.setup()

    def setup(self):
        for entity, monster in self.monster_data.items():
            for index, monster in {k: v for k, v in monster.items() if k <= 2}.items():
                self.create_monster(monster, index, index, entity)

            for i in range(len(self.opponent_sprites)):
                del self.monster_data['opponent'][i]

    def generate_linear_equation(self):
        a = random.randint(1, 10)
        x = random.randint(1, 10)
        b = random.randint(-10, 10)

        c = a * x + b

        self.current_equation = f"{a}x + {b} = {c}"
        return x

    def generate_answers(self, solution):
        wrong_answers = []
        random_answ = {random.uniform(-15, 26) for _ in range(3)}
        for i in random_answ:
            wrong_answers.append(round(i, 1))
        wrong_answers.append(solution)
        wrong_answers = list(wrong_answers)[:3]
        return [solution] + wrong_answers

    def create_monster(self, monster, index, pos_index, entity):
        frames = self.monster_frames['monsters'][monster.name]
        outline_frames = self.monster_frames['outlines'][monster.name]
        if entity == 'player':
            pos = list(BATTLE_POSITIONS['left'].values())[pos_index]
            groups = (self.battle_sprites, self.player_sprites)
            frames = {state: [pygame.transform.flip(frame, True, False) for frame in frames] for state, frames in frames.items()}
            outline_frames = {state: [pygame.transform.flip(frame, True, False) for frame in frames] for state, frames in outline_frames.items()}
        else:
            pos = list(BATTLE_POSITIONS['right'].values())[pos_index]
            groups = (self.battle_sprites, self.opponent_sprites)

        monster_sprite = MonsterSprite(pos, frames, groups, monster, index, pos_index, entity, self.apply_attack, self.create_monster)
        MonsterOutlineSprite(monster_sprite, self.battle_sprites, outline_frames)

        # ui
        name_pos = monster_sprite.rect.midleft + vector(16, -70) if entity == 'player' else \
            (monster_sprite.rect.midright+ vector(-40, -70))
        name_sprite = MonsterNameSprite(name_pos, monster_sprite, self.battle_sprites, self.fonts['regular'])
        level_pos = name_sprite.rect.bottomleft if entity == 'player' else name_sprite.rect.bottomright
        MonsterLevelSprite(entity, level_pos, monster_sprite, self.battle_sprites, self.fonts['small'])
        MonsterStatsSprite(monster_sprite.rect.midbottom + vector(0, 20), monster_sprite, (150, 48), self.battle_sprites, self.fonts['small'])

    def input(self):
        if self.selection_mode and self.current_monster:
            keys = pygame.key.get_just_pressed()

            match self.selection_mode:
                case 'general': limiter = len(BATTLE_CHOICES['full'])
                case 'attacks': limiter = len(self.current_monster.monster.get_abilities(all=False))
                case 'target': limiter = len(self.opponent_sprites) if self.selection_side == 'opponent' else len(self.player_sprites)
                case 'equation': pass

            if self.selection_mode == 'equation':
                if keys[pygame.K_RETURN]:
                    if int(self.player_answer) == self.current_solution:
                        self.equation_resolved = True
                        self.selection_mode = 'target'
                        self.player_answer = ""
                        self.selected_attack = self.current_monster.monster.get_abilities(all=False)[
                            self.indexes['attacks']]
                        self.selection_side = ATTACK_DATA[self.selected_attack]['target']
                    else:
                        self.selection_mode = 'attacks'
                        self.player_answer = ''
                elif keys[pygame.K_BACKSPACE]:
                    self.player_answer = self.player_answer[:-1]
                else:
                    for key in range(pygame.K_0, pygame.K_9 + 1):
                        if keys[key]:
                            self.player_answer += chr(key)

            if keys[pygame.K_DOWN] and self.selection_mode != 'equation':
                self.indexes[self.selection_mode] = (self.indexes[self.selection_mode] + 1) % limiter
            if keys[pygame.K_UP] and self.selection_mode != 'equation':
                self.indexes[self.selection_mode] = (self.indexes[self.selection_mode] - 1) % limiter
            if keys[pygame.K_SPACE]:
                if self.selection_mode == 'attacks':
                    self.selection_mode = 'equation'
                    self.current_solution = self.generate_linear_equation()

                if self.selection_mode == 'target':
                    self.player_answer = ''
                    sprite_group = self.opponent_sprites if self.selection_side == 'opponent' else self.player_sprites
                    sprites = {sprite.pos_index: sprite for sprite in sprite_group}
                    monster_sprite = sprites[list(sprites.keys())[self.indexes['target']]]

                    if self.selected_attack:
                        self.current_monster.activate_attack(monster_sprite, self.selected_attack)
                        self.selected_attack, self.current_monster, self.selection_mode = None, None, None

                if self.selection_mode == 'general':
                    if self.indexes['general'] == 0:
                        self.selection_mode = 'attacks'

                    if self.indexes['general'] == 1:
                        self.current_monster.monster.defending = True
                        self.update_all_monsters('resume')
                        self.current_monster, self.selection_mode = None, None
                        self.indexes['general'] = 0

                    if self.indexes['general'] == 3:
                        self.selection_mode = 'target'
                        self.selection_side = 'opponent'
                self.indexes = {k: 0 for k in self.indexes}

            if keys[pygame.K_ESCAPE]:
                if self.selection_mode in ('attacks', 'switch', 'target'):
                    self.selection_mode = 'general'

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    # battle system
    def check_active(self):
        for monster_sprite in self.player_sprites.sprites() + self.opponent_sprites.sprites():
            if monster_sprite.monster.initiative >= 100:
                monster_sprite.monster.defending = False
                self.update_all_monsters('pause')
                monster_sprite.monster.initiative = 0
                monster_sprite.set_highlight(True)
                self.current_monster = monster_sprite
                if self.player_sprites in monster_sprite.groups():
                    self.selection_mode = 'general'
                else:
                    self.timers['opponent delay'].activate()

    def update_all_monsters(self, option):
        for monster_sprite in self.player_sprites.sprites() + self.opponent_sprites.sprites():
            monster_sprite.monster.paused = True if option == 'pause' else False

    def check_death(self):
        for monster_sprite in self.opponent_sprites.sprites() + self.player_sprites.sprites():
            if monster_sprite.monster.health <= 0:
                if self.player_sprites in monster_sprite.groups():  # player
                    active_monsters = [(monster_sprite.index, monster_sprite.monster) for monster_sprite in self.player_sprites.sprites()]
                    available_monsters = [(index, monster) for index, monster in self.monster_data['player'].items()
                                          if monster.health > 0 and (index, monster) not in active_monsters]
                    if available_monsters:
                        new_monster_data = [(monster, index, monster_sprite.pos_index, 'player') for index, monster in available_monsters]
                    else:
                        new_monster_data = None
                else:
                    new_monster_data = (list(self.monster_data['opponent'].values())[0], monster_sprite.index, monster_sprite.pos_index, 'opponent') if self.monster_data['opponent'] else None
                    if self.monster_data['opponent']:
                        del self.monster_data['opponent'][min(self.monster_data['opponent'])]

                    # xp
                    xp_amount = monster_sprite.monster.level * 100 / len(self.player_sprites)
                    for player_sprite in self.player_sprites:
                        player_sprite.monster.update_xp(xp_amount)

                monster_sprite.delayed_kill(new_monster_data)

    def apply_attack(self, target_sprite, attack, amount):
        AttackSprite(target_sprite.rect.center, self.monster_frames['attacks'][ATTACK_DATA[attack]['animation']], self.battle_sprites)

        attack_element = ATTACK_DATA[attack]['element']
        target_element = target_sprite.monster.element

        target_defense = 1 - target_sprite.monster.get_stat('defense') / 2000
        if target_sprite.monster.defending:
            target_defense -= 0.2
        target_defense = max(0, min(1, target_defense))

        target_sprite.monster.health -= amount * target_defense
        self.check_death()

        # TODO use it for my mathemtaics like update_all_monsters('pause')
        self.update_all_monsters('resume')

    def check_end_battle(self):
        # opponents have been defeated
        if len(self.opponent_sprites) == 0 and not self.battle_over:
            self.battle_over = True
            self.end_battle()
            for monster in self.monster_data['player'].values():
                monster.initiative = 0

        # player has been defeated
        if len(self.player_sprites) == 0:
            pygame.quit()
            exit()

    def draw_ui(self):
        if self.current_monster:
            if self.selection_mode == 'general':
                self.draw_general()
            if self.selection_mode == 'attacks':
                self.draw_attacks()

    def equation(self):
        if self.selection_mode == 'equation':
            screen_width, screen_height = self.display_surface.get_size()

            box_width, box_height = 400, 50
            input_box = pygame.Rect(
                (screen_width - box_width) // 2,
                (screen_height - box_height) // 2 + 50,
                box_width,
                box_height
            )

            pygame.draw.rect(self.display_surface, (50, 50, 50), input_box, border_radius=10)

            font = self.fonts['regular']

            equation_text = font.render(self.current_equation, True, (255, 255, 255))
            equation_rect = equation_text.get_rect(center=(screen_width // 2, screen_height // 2 - 30))
            self.display_surface.blit(equation_text, equation_rect)

            answer_text = font.render(self.player_answer, True, (255, 255, 255))
            answer_rect = answer_text.get_rect(center=input_box.center)
            self.display_surface.blit(answer_text, answer_rect)

    def draw_general(self):
        for index, (option, data_dict) in enumerate(BATTLE_CHOICES['full'].items()):
            if index == self.indexes['general']:
                surf = self.monster_frames['ui'][f'{data_dict["icon"]}_highlight']
            else:
                surf = pygame.transform.grayscale(self.monster_frames['ui'][data_dict["icon"]])
            rect = surf.get_frect(center=self.current_monster.rect.midright + data_dict['pos'])
            self.display_surface.blit(surf, rect)

    def draw_attacks(self):
        abilities = self.current_monster.monster.get_abilities()
        width, height = 150, 50
        visible_attacks = 1
        item_height = height / visible_attacks
        v_offset = 0 if self.indexes['attacks'] < visible_attacks else -(self.indexes['attacks'] - visible_attacks + 1) * item_height

        # bg
        bg_rect = pygame.FRect((0, 0), (width, height)).move_to(midleft=self.current_monster.rect.midright + vector(20, 0))
        pygame.draw.rect(self.display_surface, COLORS['white'], bg_rect, 0, 5)

        for index, ability in enumerate(abilities):
            selected = index == self.indexes['attacks']

            if selected:
                element = ATTACK_DATA[ability]['element']
                text_color = COLORS[element] if element != 'normal' else COLORS['black']
            else:
                text_color = COLORS['light']
            text_surf = self.fonts['regular'].render(ability, False, text_color)

            text_rect = text_surf.get_frect(center=bg_rect.midtop + vector(0, item_height / 2 + index * height + v_offset))
            text_bg_rect = pygame.FRect((0, 0), (width, item_height)).move_to(center=text_rect.center)

            # draw
            if bg_rect.collidepoint(text_rect.center):
                if selected:
                    if text_bg_rect.collidepoint(bg_rect.topleft):
                        pygame.draw.rect(self.display_surface, COLORS['dark white'], text_bg_rect, 0, 0, 5, 5)
                    elif text_bg_rect.collidepoint(bg_rect.midbottom + vector(0, -1)):
                        pygame.draw.rect(self.display_surface, COLORS['dark white'], text_bg_rect, 0, 0, 0, 0, 5, 5)
                    else:
                        pygame.draw.rect(self.display_surface, COLORS['dark white'], text_bg_rect)
                self.display_surface.blit(text_surf, text_rect)

    def opponent_attack(self):
        ability = choice(self.current_monster.monster.get_abilities())
        random_target = choice(self.opponent_sprites.sprites()) if ATTACK_DATA[ability]['target'] == 'player' else (
            choice(self.player_sprites.sprites()))
        self.current_monster.activate_attack(random_target, ability)

    def update(self, dt):
        # updates
        self.check_end_battle()
        self.input()
        self.update_timers()
        self.battle_sprites.update(dt)
        self.check_active()

        # drawing
        self.display_surface.blit(self.bg_surf, (0, 0))
        self.battle_sprites.draw(self.current_monster, self.selection_side, self.selection_mode, self.indexes['target'], self.player_sprites, self.opponent_sprites)
        self.draw_ui()
        self.equation()