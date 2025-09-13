from collections import deque
from typing import Deque
from .point import Point
from .direction import Direction


class Snake:
    def __init__(self, start: Point, length: int = 3, direction = Direction.RIGHT) -> None:
        self.body: Deque[Point] = deque()
        self.direction = direction

        for i in range(length):
            self.body.append(Point(start.x - i, start.y))
    
    @property
    def head(self) -> Point:
        return self.body[0]
    
    def turn(self, new_direction: Direction) -> None:
        opposite = (self.direction.vector[0] * -1, self.direction.vector[1] * -1)
        if new_direction != opposite:
            self.direction = new_direction
    
    def move(self, grow: bool = False) -> None:
        dx, dy = self.direction.vector
        new_head = Point(self.head.x + dx, self.head.y + dy)
        self.body.appendleft(new_head)
        if not grow:
            self.body.pop()
    
    def check_self_collision(self) -> bool:
        return self.head in list(self.body)[1:]

    def check_wall_collision(self, width: int, height: int) -> bool:
        return not (0 <= self.head.x < width and 0 <= self.head.y < height)