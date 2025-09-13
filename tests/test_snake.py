import pytest
from snake_game.snake import Snake
from snake_game.point import Point
from snake_game.direction import Direction


def test_initial_snake():
    snake = Snake(start=Point(5, 5))
    assert len(snake.body) == 3
    assert snake.head == Point(5, 5)

def test_move_forward():
    snake = Snake(Point(5, 5))
    snake.move()
    assert snake.head == Point(6, 5)

def test_grow():
    snake = Snake(Point(5, 5))
    snake.move(grow=True)
    assert len(snake.body) == 4
    assert snake.head == Point(6, 5)

def test_turn_and_move():
    s = Snake(start=Point(5, 5))
    s.turn(Direction.DOWN)
    s.move()
    assert s.head == Point(5, 6)

def test_self_collision():
    s = Snake(start=Point(5, 5))
    s.turn(Direction.DOWN)
    s.move(grow=True)
    s.turn(Direction.LEFT)
    s.move(grow=True)
    s.turn(Direction.UP)
    s.move()
    assert s.check_self_collision()

def test_wall_collision():
    s = Snake(start=Point(0, 0), direction=Direction.LEFT)
    s.move()
    assert s.check_wall_collision(width=10, height=10)