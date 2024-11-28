from settings import *


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector(100, 20)

    def draw(self, player_center):
        self.offset.x = -(player_center[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(player_center[1] - WINDOW_HEIGHT / 2)

        bg_sprites = [sprite for sprite in self if sprite.z < WORLD_LAYERS['main']]
        main_sprites = sorted([sprite for sprite in self if sprite.z == WORLD_LAYERS['main']],
                              key=lambda sprite: sprite.y_sort)
        fg_sprites = [sprite for sprite in self if sprite.z > WORLD_LAYERS['main']]

        for layer in (bg_sprites, main_sprites, fg_sprites):
            for sprite in self:
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)


class BattleSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def draw(self, current_monster_sprite, side, mode, target_index, player_sprites, opponent_sprites):
        sprite_group = opponent_sprites if side == 'opponent' else player_sprites
        sprites = {sprite.pos_index: sprite for sprite in sprite_group}
        monster_sprite = sprites[list(sprites.keys())[target_index]] if sprites else None

        for sprite in sorted(self, key=lambda sprite: sprite.z):
            if sprite.z == BATTLE_LAYERS['outline']:
                if sprite.monster_sprite == current_monster_sprite and not (mode == 'target' and side == 'player') or \
                        sprite.monster_sprite == monster_sprite and sprite.monster_sprite.entity == side and mode and mode == 'target':
                    self.display_surface.blit(sprite.image, sprite.rect)
            else:
                self.display_surface.blit(sprite.image, sprite.rect)
