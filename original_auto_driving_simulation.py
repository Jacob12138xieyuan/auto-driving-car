class Car:
    def __init__(self, name, x, y, direction, commands):
        self.name = name
        self.x = x
        self.y = y
        self.direction = direction
        self.commands = commands

class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cars = []
        self.collisions = []

# Direction control system
DIRECTIONS = ['N', 'E', 'S', 'W']
DELTA = {'N': (0, 1), 'S': (0, -1), 'E': (1, 0), 'W': (-1, 0)}

def turn(current_dir, command):
    idx = DIRECTIONS.index(current_dir)
    if command == 'R':
        return DIRECTIONS[(idx + 1) % 4]
    else:  # 'L'
        return DIRECTIONS[(idx - 1) % 4]

def run_simulation(field):
    max_steps = max(len(car.commands) for car in field.cars)
    
    for step in range(max_steps):
        # Use map to store car position and find collision
        car_position_map = {}
        car_next_position_map = {}

        # Calculate new position for all cars
        for car in field.cars:
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
                    if 0 <= car.x + dx < field.width and 0 <= car.y + dy < field.height:
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
                field.collisions.append({
                    'step': step + 1,
                    'position': pos,
                    'cars': cars
                })

        # Stop simulation if collision occur   
        if field.collisions:
            return
        
        # This step no collision, update cars positions
        for car, (new_x, new_y, new_dir) in car_next_position_map.items():
            car.x = new_x
            car.y = new_y
            car.direction = new_dir

def main():   
    while True:
        # Create field
        while True:
            try:
                print("Welcome to Auto Driving Car Simulation!")
                width, height = input("\nPlease enter the width and height of the simulation field in x y format: ").split()
                width, height = int(width), int(height)
                if width <= 0 or height <= 0:
                    print("Error: Width and height must be positive integers")
                    continue
                break
            except ValueError:
                print("Error: Width and height must be integers")
        
        field = Field(width, height)
        print(f"\nYou have created a field of {width} x {height}.")
        
        # Add cars or run simulation
        while True:
            choice = input("\nPlease choose from the following options:\n[1] Add a car to field\n[2] Run simulation\n> ")
            
            if choice == '1':
                # Add cars
                while True:
                    name = input("\nPlease enter the name of the car: ").strip()
                    if not name:
                        print("Error: Name cannot be empty")
                        continue
                    if any(car.name == name for car in field.cars):
                        print("Error: A car with same name already exists")
                        continue
                    break
                
                # Get initial position and direction
                while True:
                    try:
                        x, y, dir = input(f"Please enter initial position of car {name} in x y Direction format: ").strip().split()
                        x, y, dir = int(x), int(y), dir.upper()
                        if dir not in DIRECTIONS:
                            print("Error: Direction must be N, S, E, or W")
                            continue
                        if not (0 <= x < field.width and 0 <= y < field.height):
                            print(f"Error: Position must be within field border (0-{field.width-1}, 0-{field.height-1})")
                            continue
                        break
                    except ValueError:
                        print("Error: Invalid input format, input should be like '1 2 N'.")
                
                # Get commands
                while True:
                    commands = input(f"Please enter the commands for car {name}: ")
                    if not all(c in ['F', 'L', 'R'] for c in commands):
                        print("Error: Commands can only be F, L, or R")
                        continue
                    break
                
                # Create a car object
                new_car = Car(name, x, y, dir, commands)
                field.cars.append(new_car)
                
                # Current cars in field
                print("\nYour current list of cars are:")
                for car in field.cars:
                    print(f"- {car.name}, ({car.x},{car.y}) {car.direction}, {car.commands}")
                
            elif choice == '2':
                if not field.cars:
                    print("Error: Please add at least one car first")
                    continue
                
                # Run simulation
                run_simulation(field)
                
                # Display results
                print("\nAfter simulation, the result is:")
                if field.collisions:
                    collision = field.collisions[0]
                    collided_cars = collision['cars']
                    for car in collided_cars:
                        others = [c.name for c in collided_cars if c != car]
                        print(f"- {car.name}, collides with {','.join(others)} at ({collision['position'][0]},{collision['position'][1]}) at step {collision['step']}")
                else:
                    for car in field.cars:
                        print(f"- {car.name}, ({car.x},{car.y}) {car.direction}")
                
                # Post simulation options
                while True:
                    restart = input("\nChoose:\n[1] Start over\n[2] Exit\n> ")
                    if restart == '1':
                        break  # Exit simulation loop
                    elif restart == '2':
                        print("\nThank you for running the simulation. Goodbye!")
                        return
                    else:
                        print("Error: Please enter 1 or 2")
                
                if restart == '1':
                    break  # Exit car management loop to restart
                
            else:
                print("Error: Please enter 1 or 2")

if __name__ == "__main__":
    main()