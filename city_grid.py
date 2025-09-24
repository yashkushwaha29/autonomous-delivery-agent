import numpy as np
import random
from utils import manhattan_distance

class CityGrid:
    def __init__(self, map_type="medium"):
        self.map_type = map_type
        self.size = self._get_map_size(map_type)
        self.grid = np.zeros((self.size, self.size))
        self.terrain_costs = np.ones((self.size, self.size))
        self.dynamic_obstacles = []
        self.start_pos = None
        self.goal_pos = None
        self.generate_city(map_type)
    
    def _get_map_size(self, map_type):
        sizes = {
            "small": 10,
            "medium": 15,
            "large": 20,
            "dynamic": 15
        }
        return sizes.get(map_type, 15)
    
    def generate_city(self, map_type=None):
        if map_type:
            self.map_type = map_type
            self.size = self._get_map_size(map_type)
            self.grid = np.zeros((self.size, self.size))
            self.terrain_costs = np.ones((self.size, self.size))
            self.dynamic_obstacles = []
        
        self.grid.fill(0)
        self.terrain_costs.fill(1)
        self.dynamic_obstacles = []
        
        if self.map_type == "small":
            self._generate_small_map()
        elif self.map_type == "medium":
            self._generate_medium_map()
        elif self.map_type == "large":
            self._generate_large_map()
        elif self.map_type == "dynamic":
            self._generate_dynamic_map()
        
        self._set_delivery_points()
    
    def _generate_small_map(self):
        for i in range(0, self.size, 3):
            self.grid[i, :] = 0
            self.grid[:, i] = 0
        
        buildings = [(2, 2, 2, 2), (2, 6, 2, 2), (6, 2, 2, 2), (6, 6, 2, 2)]
        for x, y, w, h in buildings:
            if x + w < self.size and y + h < self.size:
                self.grid[x:x+w, y:y+h] = -1
        
        self.terrain_costs[4:7, 4:7] = 2
        self.grid[4:7, 4:7] = 0
    
    def _generate_medium_map(self):
        for i in range(0, self.size, 4):
            self.grid[i, :] = 0
            self.grid[:, i] = 0
        
        buildings = [
            (1, 1, 3, 3), (1, 10, 3, 3), (10, 1, 3, 3), (10, 10, 3, 3),
            (5, 5, 2, 2), (5, 12, 2, 2), (12, 5, 2, 2)
        ]
        for x, y, w, h in buildings:
            if x + w < self.size and y + h < self.size:
                self.grid[x:x+w, y:y+h] = -1
        
        self.terrain_costs[3:6, 3:6] = 2
        self.terrain_costs[3:6, 9:12] = 3
        self.terrain_costs[9:12, 3:6] = 3
        self.terrain_costs[9:12, 9:12] = 2
        
        self.grid[3:6, 3:6] = 0
        self.grid[3:6, 9:12] = 0
        self.grid[9:12, 3:6] = 0
        self.grid[9:12, 9:12] = 0
    
    def _generate_large_map(self):
        for i in range(0, self.size, 4):
            self.grid[i, :] = 0
            self.grid[:, i] = 0
        
        buildings = [
            (2, 2, 3, 3), (2, 8, 3, 3), (2, 14, 3, 3),
            (8, 2, 3, 3), (8, 8, 3, 3), (8, 14, 3, 3),
            (14, 2, 3, 3), (14, 8, 3, 3), (14, 14, 3, 3),
            (5, 5, 2, 2), (5, 12, 2, 2), (12, 5, 2, 2), (12, 12, 2, 2)
        ]
        for x, y, w, h in buildings:
            if x + w < self.size and y + h < self.size:
                self.grid[x:x+w, y:y+h] = -1
        
        self.terrain_costs[4:8, 4:8] = 2
        self.terrain_costs[4:8, 12:16] = 3
        self.terrain_costs[12:16, 4:8] = 3
        self.terrain_costs[12:16, 12:16] = 2
        
        for area in [(4, 8, 4, 4), (4, 12, 4, 4), (12, 4, 4, 4), (12, 12, 4, 4)]:
            x, y, w, h = area
            self.grid[x:x+w, y:y+h] = 0
    
    def _generate_dynamic_map(self):
        for i in range(0, self.size, 3):
            self.grid[i, :] = 0
            self.grid[:, i] = 0
        
        buildings = [(3, 3, 2, 2), (3, 10, 2, 2), (10, 3, 2, 2)]
        for x, y, w, h in buildings:
            if x + w < self.size and y + h < self.size:
                self.grid[x:x+w, y:y+h] = -1
        
        self.dynamic_obstacles = [
            (2, 0, 'horizontal', 2, 2, 1),
            (0, 2, 'vertical', 3, 2, 1),
            (8, 0, 'horizontal', 4, 1, 2),
            (0, 8, 'vertical', 2, 1, 2),
            (12, 0, 'horizontal', 3, 2, 1),
            (0, 12, 'vertical', 4, 1, 1),
            (5, 0, 'horizontal', 5, 1, 1),
            (0, 5, 'vertical', 3, 2, 2)
        ]
        
        self.terrain_costs[6:9, 6:9] = 2
        self.terrain_costs[1:4, 10:13] = 3
        self.grid[6:9, 6:9] = 0
        self.grid[1:4, 10:13] = 0
    
    def _set_delivery_points(self):
        self.start_pos = self._find_empty_location()
        min_distance = self.size // 3
        self.goal_pos = self._find_empty_location(far_from=self.start_pos, min_distance=min_distance)
    
    def _find_empty_location(self, far_from=None, min_distance=0):
        max_attempts = 100
        for _ in range(max_attempts):
            x, y = random.randint(1, self.size-2), random.randint(1, self.size-2)
            if self.grid[x, y] == 0:
                if far_from:
                    distance = manhattan_distance((x, y), far_from)
                    if distance >= min_distance:
                        return (x, y)
                else:
                    return (x, y)
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x, y] == 0:
                    return (x, y)
        return (1, 1)
    
    def update_dynamic_obstacles(self, time_step):
        self.grid[self.grid == -2] = 0
        if not self.dynamic_obstacles:
            return
        for obstacle in self.dynamic_obstacles:
            pattern, interval, length, speed = obstacle[2], obstacle[3], obstacle[4], obstacle[5]
            step = (time_step // interval) * speed
            if pattern == 'horizontal':
                base_x = obstacle[0]
                base_y = 1 + (step % (self.size - 2))
                for i in range(length):
                    y_pos = (base_y + i) % (self.size - 1)
                    if y_pos < self.size and self.grid[base_x, y_pos] == 0:
                        self.grid[base_x, y_pos] = -2
            else:
                base_x = 1 + (step % (self.size - 2))
                base_y = obstacle[1]
                for i in range(length):
                    x_pos = (base_x + i) % (self.size - 1)
                    if x_pos < self.size and self.grid[x_pos, base_y] == 0:
                        self.grid[x_pos, base_y] = -2
    
    def get_grid_info(self):
        return {
            'grid': self.grid.copy(),
            'terrain_costs': self.terrain_costs.copy(),
            'start_pos': self.start_pos,
            'goal_pos': self.goal_pos,
            'size': self.size,
            'map_type': self.map_type,
            'has_dynamic_obstacles': len(self.dynamic_obstacles) > 0
        }
    
    def change_map(self, new_map_type):
        if new_map_type in ["small", "medium", "large", "dynamic"]:
            self.generate_city(new_map_type)
            return True
        return False