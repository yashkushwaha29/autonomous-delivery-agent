from queue import PriorityQueue, Queue
import time
from utils import manhattan_distance, get_neighbors, is_valid_position

class Pathfinder:
    def __init__(self, city_grid):
        self.grid = city_grid.grid
        self.terrain_costs = city_grid.terrain_costs
        self.size = city_grid.size
    
    def bfs(self, start, goal):
        if not is_valid_position(self.grid, start) or not is_valid_position(self.grid, goal):
            return None, 0
        queue = Queue()
        queue.put((start, [start]))
        visited = set([start])
        nodes_expanded = 0
        while not queue.empty():
            current, path = queue.get()
            nodes_expanded += 1
            if current == goal:
                return path, nodes_expanded
            for neighbor in get_neighbors(current, self.size):
                if (is_valid_position(self.grid, neighbor) and neighbor not in visited):
                    visited.add(neighbor)
                    queue.put((neighbor, path + [neighbor]))
        return None, nodes_expanded
    
    def uniform_cost_search(self, start, goal):
        if not is_valid_position(self.grid, start) or not is_valid_position(self.grid, goal):
            return None, 0
        pq = PriorityQueue()
        pq.put((0, start, [start]))
        visited = set()
        nodes_expanded = 0
        while not pq.empty():
            cost, current, path = pq.get()
            nodes_expanded += 1
            if current == goal:
                return path, nodes_expanded
            if current in visited:
                continue
            visited.add(current)
            for neighbor in get_neighbors(current, self.size):
                if is_valid_position(self.grid, neighbor) and neighbor not in visited:
                    new_cost = cost + self.terrain_costs[neighbor]
                    pq.put((new_cost, neighbor, path + [neighbor]))
        return None, nodes_expanded
    
    def a_star(self, start, goal):
        if not is_valid_position(self.grid, start) or not is_valid_position(self.grid, goal):
            return None, 0
        open_set = PriorityQueue()
        open_set.put((0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: manhattan_distance(start, goal)}
        open_set_hash = {start}
        nodes_expanded = 0
        while not open_set.empty():
            current = open_set.get()[1]
            open_set_hash.remove(current)
            nodes_expanded += 1
            if current == goal:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return path[::-1], nodes_expanded
            for neighbor in get_neighbors(current, self.size):
                if not is_valid_position(self.grid, neighbor):
                    continue
                tentative_g_score = g_score[current] + self.terrain_costs[neighbor]
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, goal)
                    if neighbor not in open_set_hash:
                        open_set.put((f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)
        return None, nodes_expanded
    
    def greedy_best_first(self, start, goal):
        if not is_valid_position(self.grid, start) or not is_valid_position(self.grid, goal):
            return None, 0
        pq = PriorityQueue()
        pq.put((manhattan_distance(start, goal), start, [start]))
        visited = set([start])
        nodes_expanded = 0
        while not pq.empty():
            _, current, path = pq.get()
            nodes_expanded += 1
            if current == goal:
                return path, nodes_expanded
            for neighbor in get_neighbors(current, self.size):
                if (is_valid_position(self.grid, neighbor) and neighbor not in visited):
                    visited.add(neighbor)
                    priority = manhattan_distance(neighbor, goal)
                    pq.put((priority, neighbor, path + [neighbor]))
        return None, nodes_expanded

class PathfindingResult:
    def __init__(self, algorithm_name, path, nodes_expanded, execution_time, path_cost):
        self.algorithm_name = algorithm_name
        self.path = path
        self.nodes_expanded = nodes_expanded
        self.execution_time = execution_time
        self.path_cost = path_cost
        self.success = path is not None
    
    def __str__(self):
        status = "SUCCESS" if self.success else "FAILED"
        return f"{self.algorithm_name}: {status} | Cost: {self.path_cost} | Nodes: {self.nodes_expanded} | Time: {self.execution_time:.4f}s"