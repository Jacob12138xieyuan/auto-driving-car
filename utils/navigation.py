import unittest

# Direction control system
DIRECTIONS = ['N', 'E', 'S', 'W']
DELTA = {'N': (0, 1), 'S': (0, -1), 'E': (1, 0), 'W': (-1, 0)}

def turn(current_dir, command):
    idx = DIRECTIONS.index(current_dir)
    if command == 'R':
        return DIRECTIONS[(idx + 1) % 4]
    else:  # 'L'
        return DIRECTIONS[(idx - 1) % 4]
    