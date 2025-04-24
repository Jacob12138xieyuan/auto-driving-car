import pytest
from utils.navigation import turn, DIRECTIONS

class TestNavigation:
    @pytest.mark.parametrize("current_dir, command, expected", [
        ('N', 'R', 'E'),
        ('E', 'R', 'S'),
        ('S', 'R', 'W'),
        ('W', 'R', 'N'),
        ('N', 'L', 'W'),
        ('W', 'L', 'S'),
        ('S', 'L', 'E'),
        ('E', 'L', 'N'),
    ])
    def test_turn_commands(self, current_dir, command, expected):
        """Test all turn commands produce expected results"""
        assert turn(current_dir, command) == expected

    @pytest.mark.parametrize("current_dir, commands, expected", [
        ('N', ['L', 'L'], 'S'),  # Two left turns
        ('E', ['R', 'R'], 'W'),  # Two right turns
        ('S', ['L', 'R'], 'S'),  # Left then right (no change)
        ('W', ['R', 'L', 'R'], 'N'),  # Multiple turns
    ])
    def test_multiple_turns_commands(self, current_dir, commands, expected):
        """Test chained turn commands"""
        result = current_dir
        for cmd in commands:
            result = turn(result, cmd)
        assert result == expected