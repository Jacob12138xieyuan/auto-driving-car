import unittest
from io import StringIO
from unittest.mock import patch
from entities.auto_driving_car_app import AutoDrivingCarApp


class TestUserInteraction(unittest.TestCase):
    def setUp(self):
        self.app = AutoDrivingCarApp()

    def simulate_input_output(self, inputs, expected_outputs):
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.app.run()
                output = mock_stdout.getvalue()
                for expected in expected_outputs:
                    self.assertIn(expected, output)

    def test_single_car_scenario(self):
        inputs = [
            "10 10",  # Field dimensions
            "1",  # Add car
            "A",  # Car name
            "1 2 N",  # Initial position
            "FFRFFFFRRL",  # Commands
            "2",  # Run simulation
            "2"  # Exit
        ]

        expected_outputs = [
            "Welcome to Auto Driving Car Simulation!",
            "You have created a field of 10 x 10",
            "Your current list of cars are:",
            "- A, (1,2) N, FFRFFFFRRL",
            "After simulation, the result is:",
            "- A, (5,4) S",
            "Thank you for running the simulation. Goodbye!"
        ]

        self.simulate_input_output(inputs, expected_outputs)

    def test_two_car_collision_scenario(self):
        inputs = [
            "10 10",  # Field dimensions
            "1",  # Add first car
            "A",  # Car A name
            "1 2 N",  # Initial position
            "FFRFFFFRRL",  # Commands
            "1",  # Add second car
            "B",  # Car B name
            "7 8 W",  # Initial position
            "FFLFFFFFFF",  # Commands
            "2",  # Run simulation
            "2"  # Exit
        ]

        expected_outputs = [
            "Welcome to Auto Driving Car Simulation!",
            "You have created a field of 10 x 10",
            "Your current list of cars are:",
            "- A, (1,2) N, FFRFFFFRRL",
            "Your current list of cars are:",
            "- A, (1,2) N, FFRFFFFRRL",
            "- B, (7,8) W, FFLFFFFFFF",
            "After simulation, the result is:",
            "- A, collides with B at (5,4) at step 7",
            "- B, collides with A at (5,4) at step 7",
            "Thank you for running the simulation. Goodbye!"
        ]

        self.simulate_input_output(inputs, expected_outputs)

    def test_two_car_no_collision_scenario(self):
        inputs = [
            "10 10",  # Field dimensions
            "1",  # Add first car
            "A",  # Car A name
            "1 2 N",  # Initial position
            "FFRFFFFRRL",  # Commands
            "1",  # Add second car
            "B",  # Car B name
            "7 8 W",  # Initial position
            "FFLFFFRFFF",  # Commands
            "2",  # Run simulation
            "2"  # Exit
        ]

        expected_outputs = [
            "Welcome to Auto Driving Car Simulation!",
            "You have created a field of 10 x 10",
            "Your current list of cars are:",
            "- A, (1,2) N, FFRFFFFRRL",
            "Your current list of cars are:",
            "- A, (1,2) N, FFRFFFFRRL",
            "- B, (7,8) W, FFLFFFRFFF",
            "After simulation, the result is:",
            "- A, (5,4) S",
            "- B, (2,5) W",
            "Thank you for running the simulation. Goodbye!"
        ]

        self.simulate_input_output(inputs, expected_outputs)
    
    # def test_three_car_no_collision_scenario(self):
    
    def test_boundary_handling_scenario(self):
        inputs = [
            "5 5",  # Small field
            "1",  # Add car
            "A",  # Car name
            "0 0 S",  # Initial position at edge
            "FLFR",  # Commands that would go out of bounds
            "2",  # Run simulation
            "2"  # Exit
        ]

        expected_outputs = [
            "Welcome to Auto Driving Car Simulation!",
            "You have created a field of 5 x 5",
            "Your current list of cars are:",
            "- A, (0,0) S, FLFR",
            "After simulation, the result is:",
            "- A, (1,0) S",  # Should stay at boundary
            "Thank you for running the simulation. Goodbye!",
        ]

        self.simulate_input_output(inputs, expected_outputs)

    def test_restart_simulation_scenario(self):
        inputs = [
            "5 5",  # Small field
            "1",  # Add car
            "A",  # Car name
            "0 0 S",  # Initial position at edge
            "FLFR",  # Commands that would go out of bounds
            "2",  # Run simulation
            "1",  # Restart
            "10 10",  # Field dimensions
            "1",  # Add car
            "A",  # Car name
            "1 2 N",  # Initial position
            "FFRFFFFRRL",  # Commands
            "2",  # Run simulation
            "2"  # Exit
        ]

        expected_outputs = [
            "Welcome to Auto Driving Car Simulation!",
            "You have created a field of 5 x 5",
            "Your current list of cars are:",
            "- A, (0,0) S, FLFR",
            "After simulation, the result is:",
            "- A, (1,0) S",  # Should stay at boundary
            "Welcome to Auto Driving Car Simulation!",
            "You have created a field of 10 x 10",
            "Your current list of cars are:",
            "- A, (1,2) N, FFRFFFFRRL",
            "After simulation, the result is:",
            "- A, (5,4) S",
            "Thank you for running the simulation. Goodbye!"
        ]

        self.simulate_input_output(inputs, expected_outputs)

    def test_invalid_input(self):
        inputs = [
            "0 10",  # Invalid width
            "10 10",  # Valid dimensions
            "3",  # Invalid menu choice
            "1",  # Add car
            "",  # Empty name
            "A",  # Valid name
            "1 2 X",  # Invalid direction
            "1 2 N",  # Valid position
            "FFX",  # Invalid command
            "FFRFF",  # Valid commands
            "2", "2"
        ]

        expected_outputs = [
            "Welcome to Auto Driving Car Simulation!",
            "Error: Width and height must be positive integers",
            "Welcome to Auto Driving Car Simulation!",
            "You have created a field of 10 x 10.",
            "Error: Please enter 1 or 2",
            "Error: Name cannot be empty",
            "Error: Direction must be N, S, E, or W",
            "Error: Commands can only be F, L, or R",
            "Your current list of cars are:",
            "- A, (1,2) N, FFRFF",
            "After simulation, the result is:",
            "- A, (3,4) E",
            "Thank you for running the simulation. Goodbye!"
        ]

        self.simulate_input_output(inputs, expected_outputs)

    def test_more_invalid_inputs(self):
        inputs = [
            "-1 10",  # Negative width
            "10 10",  # Valid dimensions
            "1",  # Add car
            "A",  # Valid name
            "11 2 N",  # Out of bounds x
            "1 12 N",  # Out of bounds y
            "-1 2 N",  # Negative x
            "1 -2 N",  # Negative y
            "1 2 N",  # Valid position
            "FFRFFFFRRL", # Valid commands
            "1",  # Add second car
            "A",  # Duplicate name
            "B",  # New name
            "7 8 W",  # Valid position
            "123",  # Invalid commands (numbers)
            "FFLFFFFFFF",  # Valid commands
            "2", 
            "2"
        ]

        expected_outputs = [
            "Welcome to Auto Driving Car Simulation!",
            "Error: Width and height must be positive integers",
            "Welcome to Auto Driving Car Simulation!",
            "You have created a field of 10 x 10.",
            "Error: Position must be within field border (0-9, 0-9)",
            "Error: Position must be within field border (0-9, 0-9)",
            "Error: Position must be within field border (0-9, 0-9)",
            "Error: Position must be within field border (0-9, 0-9)",
            "Your current list of cars are:",
            "- A, (1,2) N, FFRFFFFRRL",
            "Error: A car with same name already exists",
            "Error: Commands can only be F, L, or R",
            "Your current list of cars are:",
            "- A, (1,2) N, FFRFFFFRRL",
            "- B, (7,8) W, FFLFFFFFFF",
            "After simulation, the result is:",
            "- A, collides with B at (5,4) at step 7",
            "- B, collides with A at (5,4) at step 7",
            "Thank you for running the simulation. Goodbye!"
        ]

        self.simulate_input_output(inputs, expected_outputs)

    def test_empty_and_whitespace_inputs(self):
        inputs = [
            "   ",  # Empty dimensions
            "10 10",  # Valid dimensions
            "1",  # Add car
            "   ",  # Whitespace name
            "A",  # Valid name
            "  1  2  N  ",  # Extra whitespace position
            "F F L ",  # Commands with spaces
            "FFL",   # Actual commands to use
            "2", "2"
        ]

        expected_outputs = [
            "Welcome to Auto Driving Car Simulation!",
            "Error: Please enter correct format",
            "Welcome to Auto Driving Car Simulation!",
            "You have created a field of 10 x 10.",
            "Error: Name cannot be empty",
            "Error: Commands can only be F, L, or R",
            "Your current list of cars are:",
            "- A, (1,2) N, FFL"
        ]

        self.simulate_input_output(inputs, expected_outputs)


if __name__ == "__main__":
    unittest.main()
