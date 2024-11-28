from game_data import MONSTER_DATA, ATTACK_DATA
from random import randint

class Monster:
    def __init__(self, name, level):
        self.name, self.level = name, level
        self.paused = False

        # stats
        self.element = MONSTER_DATA[name]['stats']['element']
        self.base_stats = MONSTER_DATA[name]['stats']
        self.health = self.base_stats['max_health'] * self.level
        self.energy = self.base_stats['max_energy'] * self.level
        self.initiative = 0

        self.abilities = MONSTER_DATA[name]['abilities']

    def __repr__(self):
        return f'monster: {self.name}, lvl: {self.level}'

    def get_stat(self, stat):
        return self.base_stats[stat] * self.level

    def get_info(self):
        return (
            (self.health, self.get_stat('max_health')),
            (self.energy, self.get_stat('max_energy')),
            (self.initiative, 100)
        )

    def reduce_energy(self, attack):
        self.energy -= ATTACK_DATA[attack]['cost']

    def get_base_damage(self, attack):
        return self.get_stat('attack') * ATTACK_DATA[attack]['amount']

    def get_abilities(self, all=True):
        if all:
            return [ability for lvl, ability in self.abilities.items() if self.level >= lvl]
        else:
            return [ability for lvl, ability in self.abilities.items() if
                    self.level >= lvl and ATTACK_DATA[ability]['cost'] < self.energy]

    def update(self, dt):
        if not self.paused:
            self.initiative += self.get_stat('speed') * dt