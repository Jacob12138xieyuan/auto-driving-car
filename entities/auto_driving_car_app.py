from entities.field import Field
from utils.navigation import DIRECTIONS
from utils.navigation import DELTA
from utils.navigation import turn

class AutoDrivingCarApp:
    def __init__(self):
        self.field = None

    def get_field_dimensions(self):
        """Get and validate field dimensions input"""
        while True:
            try:
                width, height = input("\nPlease enter the width and height of the simulation field in x y format: ").split()
                width, height = int(width), int(height)
                if width <= 0 or height <= 0:
                    print("Error: Width and height must be positive integers")
                    continue
                return width, height
            except ValueError:
                print("Error: Please enter correct format")

    def get_main_choice(self):
        """Get user's main menu choice"""
        while True:
            choice = input("\nPlease choose from the following options:\n[1] Add a car to field\n[2] Run simulation\n> ")
            if choice in ('1', '2'):
                return choice
            print("Error: Please enter 1 or 2")

    def get_car_name(self):
        """Get and validate car name"""
        while True:
            name = input("\nPlease enter the name of the car: ").strip()
            if not name:
                print("Error: Name cannot be empty")
                continue
            if any(car.name == name for car in self.field.cars):
                print("Error: A car with same name already exists")
                continue
            return name

    def get_car_position(self):
        """Get and validate car position and direction"""
        while True:
            try:
                x, y, direction = input("Please enter initial position of car in x y Direction format: ").strip().split()
                x, y = int(x), int(y)
                direction = direction.upper()
                
                # Validate direction
                if direction not in DIRECTIONS:
                    print("Error: Direction must be N, S, E, or W")
                    continue
                    
                # Validate border
                if not (0 <= x < self.field.width and 0 <= y < self.field.height):
                    print(f"Error: Position must be within field border (0-{self.field.width-1}, 0-{self.field.height-1})")
                    continue
                    
                # Check if same position with other car
                if any(car.x == x and car.y == y for car in self.field.cars):
                    print(f"Error: Position ({x},{y}) is already occupied by another car")
                    continue
                    
                return x, y, direction
            except ValueError:
                print("Error: Invalid input format, should be like '1 2 N'")

    def get_car_commands(self):
        """Get and validate car commands"""
        while True:
            commands = input("Please enter the commands for car: ").upper()
            if all(c in {'F', 'L', 'R'} for c in commands):
                return commands
            print("Error: Commands can only be F, L, or R")

    def get_restart_choice(self):
        """Get restart/exit choice"""
        while True:
            choice = input("\nChoose:\n[1] Start over\n[2] Exit\n> ")
            if choice in ('1', '2'):
                return choice
            print("Error: Please enter 1 or 2")

    def show_simulation_results(self):
        """Display simulation results"""
        print("\nAfter simulation, the result is:")
        if self.field.collisions:
            collision = self.field.collisions[0]
            for car in collision['cars']:
                others = [c.name for c in collision['cars'] if c != car]
                print(f"- {car.name}, collides with {', '.join(others)} at ({collision['position'][0]},{collision['position'][1]}) at step {collision['step']}")
        else:
            for car in self.field.cars:
                print(f"- {car.name}, ({car.x},{car.y}) {car.direction}")

    def run_simulation(self):
        max_steps = max(len(car.commands) for car in self.field.cars)
        
        for step in range(max_steps):
            # Use map to store car position and find collision
            car_position_map = {}
            car_next_position_map = {}

            # Calculate new position for all cars
            for car in self.field.cars:
                # The car finished its commands, no position change
                if step >= len(car.commands):
                    new_x, new_y = car.x, car.y
                    new_dir = car.direction
                else:  
                    cmd = car.commands[step]
                    if cmd in ['L', 'R']:
                        new_dir = turn(car.direction, cmd)
                        new_x, new_y = car.x, car.y
                    else:  # Move forward
                        dx, dy = DELTA[car.direction]
                        # Boundary check
                        if 0 <= car.x + dx < self.field.width and 0 <= car.y + dy < self.field.height:
                            new_x = car.x + dx
                            new_y = car.y + dy
                        else:
                            new_x = car.x
                            new_y = car.y
                        new_dir = car.direction
                
                # Update next position map
                car_next_position_map[car] = (new_x, new_y, new_dir)

                # Add the car to map, later find collision
                if (new_x, new_y) in car_position_map:
                    car_position_map[(new_x, new_y)].append(car)
                else:
                    car_position_map[(new_x, new_y)] = [car]
                                    
            # Check any collisions
            for pos, cars in car_position_map.items():
                if len(cars) > 1:
                    self.field.collisions.append({
                        'step': step + 1,
                        'position': pos,
                        'cars': cars
                    })

            # Stop simulation if collision occur   
            if self.field.collisions:
                return
            
            # This step no collision, update cars positions
            for car, (new_x, new_y, new_dir) in car_next_position_map.items():
                car.x = new_x
                car.y = new_y
                car.direction = new_dir

    def run(self):
        while True:
            print("Welcome to Auto Driving Car Simulation!")
            
            # Initialize field
            width, height = self.get_field_dimensions()
            self.field = Field(width, height)
            print(f"\nYou have created a field of {width} x {height}.")

            while True:
                # Car adding or run simulation
                choice = self.get_main_choice()

                if choice == '1':
                    # Add car
                    name = self.get_car_name()
                    x, y, direction = self.get_car_position()
                    commands = self.get_car_commands()
                    
                    self.field.add_car(name, x, y, direction, commands)
                    self.field.show_cars()

                elif choice == '2':
                    # Run simulation
                    if not self.field.cars:
                        print("Error: Please add at least one car first")
                        continue

                    self.run_simulation()
                    self.show_simulation_results()

                    # Post-simulation flow
                    if self.get_restart_choice() == '1':
                        break  # Restart simulation
                    else:
                        print("\nThank you for running the simulation. Goodbye!")
                        return