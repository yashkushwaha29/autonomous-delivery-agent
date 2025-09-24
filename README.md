Autonomous Delivery Agent Simulator - README
 This project implements an Autonomous Delivery Agent Simulator with multiple city grid maps,
 dynamic obstacles, and various pathfinding algorithms. The system simulates delivery agents
 navigating through urban environments using intelligent search strategies. The purpose of this
 simulator is to provide a visual and interactive way to study how different pathfinding algorithms
 perform under static and dynamic conditions. It is designed for learning, research, and
 experimentation with AI search methods.
 Features:
 • City grid generation with four map types: Small, Medium, Large, Dynamic.
 • Dynamic obstacle handling for simulating moving traffic or barriers.
 • Multiple pathfinding algorithms: BFS, Uniform Cost Search, A*, Greedy Best-First.
 • Interactive visualization using Matplotlib with map and algorithm selection.
 • Detailed performance metrics: path cost, nodes expanded, execution time.
 • Terrain costs for different environments (roads, grass, mud).
 • Reset and step-based simulation control.
Project Structure:
 File
 main.py
 city_grid.py
 simulation.py
 pathfinding.py
 utils.py
 Description
 Entry point of the application; initializes the simulator.
 Handles city grid generation, map types, and obstacles.
 Manages simulation flow, time steps, and integrates pathfinding.
 Implements BFS, UCS, A*, and Greedy Best-First algorithms.
 visualization.py Provides interactive Matplotlib-based visualization.
 Contains helper functions like distance calculations and path cost.
 Pathfinding Algorithms:
 1. Breadth-First Search (BFS): Explores all neighbors at the present depth prior to moving on to
 the next level. Guarantees the shortest path in unweighted grids.
 2. Uniform Cost Search (UCS): Expands the least costly node first. It takes terrain costs into
 account, making it suitable for weighted grids.
 3. A* Search: Combines UCS with heuristics (Manhattan distance). It balances path cost and
 heuristic distance, making it efficient and optimal.
 4. Greedy Best-First Search: Selects paths that appear best in the short term by minimizing
 heuristic distance. Faster but not always optimal.
How to Run the Project:
 1. Install the required dependencies (e.g., matplotlib, numpy, reportlab).
 2. Run main.py using Python:
 python main.py
 3. Use the UI to select a map type and pathfinding algorithm.
 4. Click 'Find Path' to compute the route from the start to the goal.
 5. Use 'Next Time Step' and 'Previous Step' to simulate dynamic obstacles.
 6. View results including path cost, nodes expanded, and execution time.
 The visualization highlights different grid elements:- Green: Start position- Red: Goal position- Gray: Buildings (static obstacles)- Orange: Traffic (dynamic obstacles)- Light Green: Grass (cost 2)- Brown: Mud (cost 3)
Requirements:
 • Python 3.8+
 • matplotlib
 • numpy
 • reportlab
 Future Enhancements:
 • Add support for diagonal movements and weighted heuristics.
 • Introduce real-time agent animation in the visualization.
 • Support for multiple delivery agents navigating simultaneously.
 • Integration with reinforcement learning for adaptive navigation.
 • Add performance comparison charts for different algorithms.
 • Export results to CSV or JSON for analysis.
 This project provides a foundation for experimenting with pathfinding algorithms and autonomous
 agent simulations in dynamic city environments. It is extensible for further research in robotics, AI,
 and transportation systems
