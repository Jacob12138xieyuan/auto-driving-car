from entities.Car import Car

class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cars = []
        self.collisions = []

    def add_car(self, name, x, y, direction, commands):
        self.cars.append(Car(name, x, y, direction, commands))

    def show_cars(self):
        """Display current list of cars"""
        print("\nYour current list of cars are:")
        for car in self.cars:
            print(f"- {car.name}, ({car.x},{car.y}) {car.direction}, {car.commands}")
