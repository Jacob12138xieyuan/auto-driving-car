import pytest
from entities.Field import Field
from entities.Car import Car
from utils.simulation import run_simulation

@pytest.fixture
def empty_field():
    """Fixture providing an empty 10x10 field"""
    return Field(10, 10)

class TestSimulation:
    @pytest.mark.parametrize("car, expected_x, expected_y, expected_dir", [
        (Car("A", 1, 2, "N", "FFRFFFFRRL"), 5, 4, 'S'),
        (Car("B", 0, 0, "E", "FFLFF"), 2, 2, 'N'),
        (Car("C", 5, 5, "W", "RRRR"), 5, 5, 'W')  # Full circle turns
    ])
    def test_single_car_movement(self, empty_field, car, expected_x, expected_y, expected_dir):
        """Test various single car movement scenarios"""
        empty_field.cars.append(car)
        run_simulation(empty_field)
        assert car.x == expected_x
        assert car.y == expected_y
        assert car.direction == expected_dir
        assert len(empty_field.collisions) == 0

    @pytest.mark.parametrize("cars, expected_collision_pos", [
        ([Car("A", 1, 2, "N", "FFRFFFFRRL"), Car("B", 7, 8, "W", "FFLFFFFFFF")], (5, 4)),
        ([Car("X", 5, 5, "N", "F"), Car("Y", 5, 7, "S", "F")], (5, 6)),
        ([Car("P", 0, 0, "E", "FF"), Car("Q", 2, 0, "W", "F")], (1, 0))
    ])
    def test_two_cars_collision_scenarios(self, empty_field, cars, expected_collision_pos):
        """Test different collision scenarios"""
        empty_field.cars.extend(cars)
        run_simulation(empty_field)
        assert len(empty_field.collisions) == 1
        assert empty_field.collisions[0]['position'] == expected_collision_pos

    @pytest.mark.parametrize("cars, expected_final_pos", [
    ([Car("A", 1, 2, "N", "FFRFFFFRRL"), Car("B", 7, 8, "W", "FFLFFFRFFF")], 
     [(5, 4, 'S'), (2, 5, 'W')])
    ])
    def test_two_cars_no_collision(self, empty_field, cars, expected_final_pos):
        """Test multiple non-colliding car scenarios"""
        empty_field.cars.extend(cars)
        run_simulation(empty_field)
        
        assert len(empty_field.collisions) == 0
        
        for car, (exp_x, exp_y, exp_dir) in zip(cars, expected_final_pos):
            assert car.x == exp_x
            assert car.y == exp_y
            assert car.direction == exp_dir

    @pytest.mark.parametrize("start_x, start_y, direction, commands, expected_x, expected_y", [
        (0, 0, "S", "FLFR", 1, 0),  # Hits bottom boundary
        (9, 9, "N", "FF", 9, 9),    # Hits top boundary
        (0, 5, "W", "F", 0, 5),     # Hits left boundary
        (9, 5, "E", "FF", 9, 5)     # Hits right boundary
    ])
    def test_boundary_handling(self, empty_field, start_x, start_y, direction, commands, expected_x, expected_y):
        """Test various boundary conditions"""
        car = Car("BoundaryTest", start_x, start_y, direction, commands)
        empty_field.cars.append(car)
        run_simulation(empty_field)
        assert car.x == expected_x
        assert car.y == expected_y