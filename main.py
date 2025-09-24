from city_grid import CityGrid
from simulation import Simulation
from visualization import CityVisualizer

def main():
    print("Starting Autonomous Delivery Agent Simulator...")
    
    city = CityGrid(map_type="medium")
    simulation = Simulation(city)
    visualizer = CityVisualizer(simulation)
    
    print("Simulator started successfully!")
    visualizer.show()

if __name__ == "__main__":
    main()