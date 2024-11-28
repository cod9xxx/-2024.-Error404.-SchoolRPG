import pygame

from settings import *

class MonsterIndex:
    def __init__(self, monsters, fonts, monster_frames):
        self.display_surface = pygame.display.get_surface()
        self.fonts = fonts
        self.monsters = monsters

        # frames
        self.icon_frames = monster_frames['icons']


        # tint surf
        self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_surf.set_alpha(200)

        # dimensions
        self.main_rect = pygame.FRect(0, 0, WINDOW_WIDTH * 0.6, WINDOW_HEIGHT * 0.8).move_to(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # list
        self.visible_items = 6
        self.list_width = self.main_rect.width * 0.3
        self.item_height = self.main_rect.height / self.visible_items
        self.index = 0
        self.selected_index = None

    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_UP]:
            self.index -= 1
        if keys[pygame.K_DOWN]:
            self.index += 1
        if keys[pygame.K_SPACE]:
            if self.selected_index != None:
                selected_monster = self.monsters[self.selected_index]
                current_monster = self.monsters[self.index]
                self.monsters[self.index] = selected_monster
                self.monsters[self.selected_index] = current_monster
                self.selected_index = None
            else:
                self.selected_index = self.index

        self.index = self.index & len(self.monsters)

    def display_list(self):
        v_offset = 0 if self.index < self.visible_items else (self.index - self.visible_items + 1) * self.item_height
        for index, monster in self.monsters.items():
            # colors
            bg_color = COLORS['gray'] if self.index != index else COLORS['light']
            text_color = COLORS['white'] if self.selected_index != index else COLORS['gold']

            top = self.main_rect.top + index * self.item_height + v_offset
            item_rect = pygame.FRect(self.main_rect.left, top, self.list_width, self.item_height)

            text_surf = self.fonts['regular'].render(monster.name, False, text_color)
            text_rect = text_surf.get_frect(midleft=item_rect.midleft + vector(90, 0))

            icon_surf = self.icon_frames[monster.name]
            icon_rect = icon_surf.get_frect(center=item_rect.midleft + vector(45, 0))

            if item_rect.colliderect(self.main_rect):
                # check corners
                if item_rect.collidepoint(self.main_rect.topleft):
                    pygame.draw.rect(self.display_surface, bg_color, item_rect, 0, 0, 12)
                elif item_rect.collidepoint(self.main_rect.bottomleft + vector(1, - 1)):
                    pygame.draw.rect(self.display_surface, bg_color, item_rect, 0, 0, 0, 0, 12, 0)
                else:
                    pygame.draw.rect(self.display_surface, bg_color, item_rect)

                self.display_surface.blit(text_surf, text_rect)
                self.display_surface.blit(icon_surf, icon_rect)

    def update(self, dt):
        self.input()
        self.display_surface.blit(self.tint_surf, (0, 0))
        self.display_list()
        # display the main section
