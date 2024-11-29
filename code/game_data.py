LESSONS_INFO = {
    '1': 'Линейные и квадратные уравнения',
}

MONSTER_DATA = {
    'Игрок': {
        'stats': {'element': 'plant', 'max_health': 15, 'max_energy': 17, 'attack': 4, 'defense': 8, 'recovery': 1,
                  'speed': 1},
        'abilities': {0: 'царапать'},
        'evolve': None},
    'Фея': {
        'stats': {'element': 'plant', 'max_health': 15, 'max_energy': 17, 'attack': 4, 'defense': 8, 'recovery': 1,
                  'speed': 1},
        'abilities': {0: 'лёд'},
        'evolve': ('Ivieron', 15)},
    'Ivieron': {
        'stats': {'element': 'plant', 'max_health': 18, 'max_energy': 20, 'attack': 5, 'defense': 10, 'recovery': 1.2,
                  'speed': 1.2},
        'abilities': {0: 'scratch', 5: 'spark'},
        'evolve': ('Pluma', 32)},
    'Pluma': {
        'stats': {'element': 'plant', 'max_health': 23, 'max_energy': 26, 'attack': 6, 'defense': 12, 'recovery': 1.8,
                  'speed': 1.8},
        'abilities': {0: 'scratch', 5: 'spark'},
        'evolve': None},
    'Sparchu': {
        'stats': {'element': 'fire', 'max_health': 15, 'max_energy': 7, 'attack': 3, 'defense': 8, 'recovery': 1.1,
                  'speed': 1},
        'abilities': {0: 'scratch', 5: 'fire', 15: 'battlecry', 26: 'explosion'},
        'evolve': ('Cindrill', 15)},
    'КубоСлайм': {
        'stats': {'element': 'fire', 'max_health': 18, 'max_energy': 10, 'attack': 3.5, 'defense': 10, 'recovery': 1.2,
                  'speed': 1.1},
        'abilities': {0: 'царапать', 5: 'fire', 15: 'battlecry', 26: 'explosion'},
        'evolve': ('Charmadillo', 33)},
    'Charmadillo': {
        'stats': {'element': 'fire', 'max_health': 29, 'max_energy': 12, 'attack': 4, 'defense': 17, 'recovery': 1.35,
                  'speed': 1.1},
        'abilities': {0: 'scratch', 5: 'fire', 15: 'battlecry', 26: 'explosion', 45: 'annihilate'},
        'evolve': None},
    'Finsta': {
        'stats': {'element': 'water', 'max_health': 13, 'max_energy': 17, 'attack': 2, 'defense': 8, 'recovery': 1.5,
                  'speed': 1.8},
        'abilities': {0: 'scratch', 5: 'spark', 15: 'splash', 20: 'ice', 25: 'heal'},
        'evolve': None},
    'Gulfin': {
        'stats': {'element': 'water', 'max_health': 18, 'max_energy': 20, 'attack': 3, 'defense': 10, 'recovery': 1.8,
                  'speed': 2},
        'abilities': {0: 'scratch', 5: 'spark', 15: 'splash', 20: 'ice', 25: 'heal'},
        'evolve': ('Finiette', 45)},
    'Finiette': {
        'stats': {'element': 'water', 'max_health': 27, 'max_energy': 23, 'attack': 4, 'defense': 17, 'recovery': 2,
                  'speed': 2.5},
        'abilities': {0: 'scratch', 5: 'spark', 15: 'splash', 20: 'ice', 25: 'heal'},
        'evolve': None},
    'Atrox': {
        'stats': {'element': 'fire', 'max_health': 18, 'max_energy': 20, 'attack': 3, 'defense': 10, 'recovery': 1.3,
                  'speed': 1.9},
        'abilities': {0: 'scratch', 5: 'spark', 30: 'fire'},
        'evolve': None},
    'МагТематик': {
        'stats': {'element': 'plant', 'max_health': 23, 'max_energy': 25, 'attack': 4, 'defense': 12, 'recovery': 1,
                  'speed': 1.5},
        'abilities': {0: 'царапать', 5: 'spark', 25: 'heal'},
        'evolve': None},
    'Draem': {
        'stats': {'element': 'plant', 'max_health': 23, 'max_energy': 25, 'attack': 4, 'defense': 12, 'recovery': 1.2,
                  'speed': 1.4},
        'abilities': {0: 'scratch', 5: 'heal', 20: 'explosion', 25: 'splash'},
        'evolve': None},
    'КвадратоСлайм': {
        'stats': {'element': 'plant', 'max_health': 15, 'max_energy': 17, 'attack': 1, 'defense': 8, 'recovery': 1,
                  'speed': 1},
        'abilities': {0: 'царапать', 5: 'spark'},
        'evolve': ('Cleaf', 4)},
    'Cleaf': {
        'stats': {'element': 'plant', 'max_health': 18, 'max_energy': 20, 'attack': 3, 'defense': 10, 'recovery': 1.7,
                  'speed': 1.6},
        'abilities': {0: 'scratch', 5: 'heal'},
        'evolve': None},
    'Jacana': {
        'stats': {'element': 'fire', 'max_health': 12, 'max_energy': 19, 'attack': 3, 'defense': 10, 'recovery': 2.1,
                  'speed': 2.6},
        'abilities': {0: 'scratch', 5: 'spark', 15: 'burn', 20: 'explosion', 25: 'heal'},
        'evolve': None},
    'Friolera': {
        'stats': {'element': 'water', 'max_health': 13, 'max_energy': 20, 'attack': 4, 'defense': 6, 'recovery': 1.3,
                  'speed': 2},
        'abilities': {0: 'scratch', 5: 'spark', 15: 'splash', 20: 'ice', 25: 'heal'},
        'evolve': None},
}

ATTACK_DATA = {
    'burn': {'target': 'opponent', 'amount': 2, 'cost': 15, 'element': 'fire', 'animation': 'fire'},
    'heal': {'target': 'player', 'amount': -1.2, 'cost': 600, 'element': 'plant', 'animation': 'green'},
    'battlecry': {'target': 'player', 'amount': -1.4, 'cost': 20, 'element': 'normal', 'animation': 'green'},
    'spark': {'target': 'opponent', 'amount': 1.1, 'cost': 20, 'element': 'fire', 'animation': 'fire'},
    'царапать': {'target': 'opponent', 'amount': 1.2, 'cost': 20, 'element': 'normal', 'animation': 'царапать'},
    'splash': {'target': 'opponent', 'amount': 2, 'cost': 15, 'element': 'water', 'animation': 'splash'},
    'fire': {'target': 'opponent', 'amount': 2, 'cost': 15, 'element': 'fire', 'animation': 'fire'},
    'explosion': {'target': 'opponent', 'amount': 2, 'cost': 90, 'element': 'fire', 'animation': 'explosion'},
    'annihilate': {'target': 'opponent', 'amount': 3, 'cost': 30, 'element': 'fire', 'animation': 'explosion'},
    'лёд': {'target': 'opponent', 'amount': 2, 'cost': 15, 'element': 'water', 'animation': 'лёд'},
}
