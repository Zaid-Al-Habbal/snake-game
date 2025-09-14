from snake_game.snake import Snake
from snake_game.point import Point
from snake_game.food import Food
from snake_game.settings import GRID_WIDTH, GRID_HEIGHT


def test_food_position_within_bounds():
    s = Snake(start=Point(5, 5))
    f = Food.random_food(s)
    assert 0 <= f.position.x < GRID_WIDTH
    assert 0 <= f.position.y < GRID_HEIGHT

def test_food_not_on_snake():
    s = Snake(start=Point(5, 5))
    # artificially grow snake across a lot of cells
    for _ in range(10):
        s.move(grow=True)
    f = Food.random_food(s)
    assert f.position not in s.body