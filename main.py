from entities.Field import Field
from entities.Car import Car
from utils.navigation import DIRECTIONS
from utils.simulation import run_simulation

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
