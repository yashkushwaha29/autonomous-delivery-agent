import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons
import numpy as np

class CityVisualizer:
    def __init__(self, simulation):
        self.simulation = simulation
        self.fig = None
        self.ax = None
        self.control_ax = None
        self.setup_ui()
    
    def setup_ui(self):
        self.fig = plt.figure(figsize=(16, 14))
        self.fig.suptitle('Autonomous Delivery Agent Simulator', fontsize=16, y=0.97)

        self.ax = plt.axes([0.05, 0.45, 0.65, 0.5])  

        self.legend_ax = plt.axes([0.72, 0.45, 0.25, 0.5])
        self.legend_ax.axis('off')

        self.results_ax = plt.axes([0.05, 0.3, 0.4, 0.12])
        self.results_ax.axis('off')

        algo_ax = plt.axes([0.05, 0.18, 0.25, 0.1])
        self.algorithm_selector = RadioButtons(algo_ax, ['BFS', 'Uniform Cost', 'A*', 'Greedy Best-First'])
        self.algorithm_selector.set_active(2)

        map_ax = plt.axes([0.35, 0.18, 0.25, 0.1])
        self.map_selector = RadioButtons(map_ax, ['Small', 'Medium', 'Large', 'Dynamic'])
        self.map_selector.set_active(1)

        self.find_path_btn = Button(plt.axes([0.72, 0.22, 0.12, 0.04]), 'Find Path')
        self.reset_btn = Button(plt.axes([0.85, 0.22, 0.12, 0.04]), 'Reset Map')
        self.next_step_btn = Button(plt.axes([0.72, 0.17, 0.12, 0.04]), 'Next Step')
        self.step_back_btn = Button(plt.axes([0.85, 0.17, 0.12, 0.04]), 'Previous Step')

        self.info_ax = plt.axes([0.5, 0.3, 0.45, 0.12])
        self.info_ax.axis('off')

        self.algorithm_selector.on_clicked(self.on_algorithm_change)
        self.map_selector.on_clicked(self.on_map_change)
        self.find_path_btn.on_clicked(self.on_find_path)
        self.reset_btn.on_clicked(self.on_reset)
        self.next_step_btn.on_clicked(self.on_next_step)
        self.step_back_btn.on_clicked(self.on_previous_step)
        
        self.update_display()
    
    def on_algorithm_change(self, label):
        self.simulation.set_algorithm(label)
        self.update_display()
    
    def on_map_change(self, label):
        map_types = {"Small": "small", "Medium": "medium", "Large": "large", "Dynamic": "dynamic"}
        new_map_type = map_types[label]
        success = self.simulation.set_map(new_map_type)
        if success:
            self.update_display()
    
    def on_find_path(self, event):
        result = self.simulation.run_pathfinding()
        print(result)
        self.update_display()
    
    def on_reset(self, event):
        self.simulation.reset_simulation()
        self.update_display()
    
    def on_next_step(self, event):
        new_time = self.simulation.next_time_step()
        print(f"Time step: {new_time}")
        self.update_display()
    
    def on_previous_step(self, event):
        new_time = self.simulation.previous_time_step()
        print(f"Time step: {new_time}")
        self.update_display()
    
    def update_display(self):

        self.ax.clear()
        self.legend_ax.clear()
        self.results_ax.clear()
        self.info_ax.clear()
        
        grid_info = self.simulation.city_grid.get_grid_info()
        grid = grid_info['grid']
        terrain_costs = grid_info['terrain_costs']
        start_pos = grid_info['start_pos']
        goal_pos = grid_info['goal_pos']
        size = grid_info['size']
        map_type = grid_info['map_type']
        has_dynamic = grid_info['has_dynamic_obstacles']

        vis_grid = np.zeros((size, size, 3))
        
        for i in range(size):
            for j in range(size):
                if (i, j) == start_pos:
                    vis_grid[i, j] = [0, 1, 0]  
                elif (i, j) == goal_pos:
                    vis_grid[i, j] = [1, 0, 0] 
                elif grid[i, j] == -1:
                    vis_grid[i, j] = [0.3, 0.3, 0.3] 
                elif grid[i, j] == -2:
                    vis_grid[i, j] = [1, 0.5, 0]  
                elif terrain_costs[i, j] == 2:
                    vis_grid[i, j] = [0.7, 1, 0.7] 
                elif terrain_costs[i, j] == 3:
                    vis_grid[i, j] = [0.6, 0.4, 0.2]  
                else:
                    vis_grid[i, j] = [0.9, 0.9, 0.9]  

        self.ax.imshow(vis_grid, origin='upper', extent=[0, size, 0, size])

        if self.simulation.current_path:
            path_y = [pos[0] for pos in self.simulation.current_path]
            path_x = [pos[1] for pos in self.simulation.current_path]
            self.ax.plot([x + 0.5 for x in path_x], [y + 0.5 for y in path_y], 
                        'b-', linewidth=3, alpha=0.8, label='Path')
            self.ax.scatter([x + 0.5 for x in path_x], [y + 0.5 for y in path_y], 
                           c='blue', s=50, alpha=0.6)

        self.ax.set_xticks(np.arange(0, size + 1, 1))
        self.ax.set_yticks(np.arange(0, size + 1, 1))
        self.ax.grid(True, color='black', linestyle='-', linewidth=0.5, alpha=0.3)

        title = f'City Map: {map_type.title()} ({size}x{size}) | Time Step: {self.simulation.time_step} | Algorithm: {self.simulation.current_algorithm}'
        if has_dynamic:
            title += " | Dynamic Objects"
        self.ax.set_title(title, fontsize=14, pad=10)

        self.legend_ax.axis('off')
        legend_title = "MAP LEGEND"
        self.legend_ax.text(0.1, 0.95, legend_title, fontsize=14, fontweight='bold', 
                           bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))

        legend_items = [
            ('Start Position', 'green'),
            ('Goal Position', 'red'),
            ('Buildings (Blocked)', 'darkgray'),
            ('Moving Vehicles', 'orange'),
            ('Grass (Cost: 2)', 'lightgreen'),
            ('Mud (Cost: 3)', 'brown'),
            ('Roads (Cost: 1)', 'lightgray'),
            ('Calculated Path', 'blue')
        ]
        
        y_positions = [0.85, 0.75, 0.65, 0.55, 0.45, 0.35, 0.25, 0.15]
        
        for i, (label, color) in enumerate(legend_items):
            y_pos = y_positions[i]

            self.legend_ax.add_patch(plt.Rectangle((0.1, y_pos-0.03), 0.08, 0.06, 
                                                 facecolor=color, edgecolor='black'))
         
            self.legend_ax.text(0.25, y_pos, label, fontsize=11, verticalalignment='center')

        self.results_ax.axis('off')
        results_title = "PATHFINDING RESULTS"
        self.results_ax.text(0.02, 0.85, results_title, fontsize=13, fontweight='bold',
                           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
        
        if self.simulation.results_history:
            latest_result = self.simulation.results_history[-1]
            status_icon = "✅ SUCCESS" if latest_result.success else "❌ FAILED"
            status_color = "green" if latest_result.success else "red"
            
            results_text = (f"Algorithm: {latest_result.algorithm_name}\n"
                          f"Status: {status_icon}\n"
                          f"Path Cost: {latest_result.path_cost}\n"
                          f"Nodes Expanded: {latest_result.nodes_expanded}\n"
                          f"Execution Time: {latest_result.execution_time:.4f}s\n"
                          f"Path Length: {len(latest_result.path) if latest_result.path else 0} steps")
        else:
            results_text = "No path calculated yet.\nClick 'Find Path' to start!"
        
        self.results_ax.text(0.02, 0.5, results_text, fontsize=11, verticalalignment='top',
                           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
        
        self.info_ax.axis('off')
        info_title = "MAP INFORMATION"
        self.info_ax.text(0.02, 0.85, info_title, fontsize=13, fontweight='bold',
                         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        
        map_descriptions = {
            "small": "Simple 10x10 layout for quick testing and algorithm learning",
            "medium": "Balanced 15x15 city with varied terrain and obstacles", 
            "large": "Complex 20x20 urban environment with extensive road network",
            "dynamic": "15x15 map with moving vehicles - paths change over time!"
        }
        
        algorithm_descriptions = {
            "BFS": "Finds shortest path by steps, ignores terrain costs",
            "Uniform Cost": "Finds cheapest path considering terrain costs", 
            "A*": "Optimal balance of speed and cost efficiency (recommended)",
            "Greedy Best-First": "Fast but may not find optimal path"
        }
        
        info_text = (f"Current Map: {map_type.title()} ({size}x{size})\n"
                    f"Dynamic Objects: {'Yes' if has_dynamic else 'No'}\n"
                    f"Time Step: {self.simulation.time_step}\n"
                    f"\nMap Type: {map_descriptions[map_type]}\n"
                    f"Algorithm: {algorithm_descriptions[self.simulation.current_algorithm]}")
        
        self.info_ax.text(0.02, 0.5, info_text, fontsize=10, verticalalignment='top',
                         bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.7))
        
        plt.draw()
    
    def show(self):
        plt.show()