import pytest
from entities.Car import Car

class TestCar:
    @pytest.mark.parametrize("name,x,y,direction,commands", [
        ("Car1", 0, 0, "N", ""),
        ("Car2", 5, 5, "E", "FFLFF"),
        ("Car3", 9, 9, "S", "RRR")
    ])
    def test_multiple_car_initializations(self, name, x, y, direction, commands):
        car = Car(name, x, y, direction, commands)
        assert car.name == name
        assert car.x == x
        assert car.y == y
        assert car.direction == direction
        assert car.commands == commands