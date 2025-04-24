from utils.navigation import DELTA
from utils.navigation import turn

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