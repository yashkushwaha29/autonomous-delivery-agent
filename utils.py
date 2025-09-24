import numpy as np
import random
import math

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def euclidean_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def is_valid_position(grid, position):
    x, y = position
    rows, cols = grid.shape
    return (0 <= x < rows and 0 <= y < cols and grid[x, y] >= 0)

def get_neighbors(position, grid_size):
    x, y = position
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid_size and 0 <= ny < grid_size:
            neighbors.append((nx, ny))
    return neighbors

def calculate_path_cost(path, terrain_costs):
    if not path or len(path) < 2:
        return 0
    total_cost = 0
    for i in range(1, len(path)):
        x, y = path[i]
        total_cost += terrain_costs[x, y]
    return total_cost