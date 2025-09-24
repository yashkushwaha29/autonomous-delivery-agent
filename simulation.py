import time
from pathfinding import Pathfinder, PathfindingResult
from utils import calculate_path_cost

class Simulation:
    def __init__(self, city_grid):
        self.city_grid = city_grid
        self.pathfinder = Pathfinder(city_grid)
        self.current_algorithm = "A*"
        self.time_step = 0
        self.current_path = None
        self.results_history = []
    
    def set_algorithm(self, algorithm_name):
        valid_algorithms = ["BFS", "Uniform Cost", "A*", "Greedy Best-First"]
        if algorithm_name in valid_algorithms:
            self.current_algorithm = algorithm_name
            return True
        return False
    
    def set_map(self, map_type):
        success = self.city_grid.change_map(map_type)
        if success:
            self.time_step = 0
            self.current_path = None
            self.results_history = []
        return success
    
    def run_pathfinding(self):
        self.city_grid.update_dynamic_obstacles(self.time_step)
        start_time = time.time()
        
        if self.current_algorithm == "BFS":
            path, nodes_expanded = self.pathfinder.bfs(self.city_grid.start_pos, self.city_grid.goal_pos)
        elif self.current_algorithm == "Uniform Cost":
            path, nodes_expanded = self.pathfinder.uniform_cost_search(self.city_grid.start_pos, self.city_grid.goal_pos)
        elif self.current_algorithm == "A*":
            path, nodes_expanded = self.pathfinder.a_star(self.city_grid.start_pos, self.city_grid.goal_pos)
        elif self.current_algorithm == "Greedy Best-First":
            path, nodes_expanded = self.pathfinder.greedy_best_first(self.city_grid.start_pos, self.city_grid.goal_pos)
        
        execution_time = time.time() - start_time
        path_cost = calculate_path_cost(path, self.city_grid.terrain_costs) if path else 0
        
        result = PathfindingResult(self.current_algorithm, path, nodes_expanded, execution_time, path_cost)
        self.current_path = path
        self.results_history.append(result)
        return result
    
    def next_time_step(self):
        self.time_step += 1
        self.current_path = None
        return self.time_step
    
    def previous_time_step(self):
        if self.time_step > 0:
            self.time_step -= 1
            self.current_path = None
        return self.time_step
    
    def reset_simulation(self):
        self.time_step = 0
        self.current_path = None
        self.results_history = []
        self.city_grid.generate_city()
    
    def get_simulation_state(self):
        return {
            'time_step': self.time_step,
            'algorithm': self.current_algorithm,
            'map_type': self.city_grid.map_type,
            'has_path': self.current_path is not None,
            'grid_info': self.city_grid.get_grid_info(),
            'current_path': self.current_path,
            'has_dynamic_obstacles': len(self.city_grid.dynamic_obstacles) > 0
        }