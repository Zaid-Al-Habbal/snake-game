import random
from .point import Point
from .snake import Snake
from .settings import GRID_HIGHT, GRID_WIDTH


class Food:
    def __init__(self, position: Point) -> None:
        self.position = position

    @classmethod
    def random_food(cls, snake: Snake) -> 'Food':
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HIGHT - 1)
            food_position = Point(x, y)
            if food_position not in snake.body:
                return cls(food_position)
        