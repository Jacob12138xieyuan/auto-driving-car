import pytest
from entities.field import Field
from entities.car import Car

class TestField:
    @pytest.mark.parametrize("width,height", [
        (5, 5),
        (10, 20),
        (100, 100),
        (1, 1)
    ])
    def test_field_dimensions(self, width, height):
        """Test field initialization with different dimensions"""
        field = Field(width, height)
        assert field.width == width
        assert field.height == height

    def test_multiple_cars(self):
        """Test adding multiple cars to the field"""
        car1 = Car("A", 1, 2, "N", "")
        car2 = Car("B", 7, 8, "W", "FFLFF")
        field = Field(10, 10)
        field.cars.extend([car1, car2])
        
        assert len(field.cars) == 2
        assert field.cars[0].name == "A"
        assert field.cars[1].name == "B"

    # def test_invalid_dimensions(self):
    #     """Test field initialization with invalid dimensions"""
    #     with pytest.raises(ValueError):
    #         Field(0, 10)
    #     with pytest.raises(ValueError):
    #         Field(10, -5)