import sys
import pygame
from .snake import Snake
from .food import Food
from .point import Point
from .direction import Direction
from . import settings


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.GRID_WIDTH * settings.CELL_SIZE,
             settings.GRID_HEIGHT * settings.CELL_SIZE)
        )
        pygame.display.set_caption("Snake Game")

        self.clock = pygame.time.Clock()
        self.snake = Snake(start=Point(settings.GRID_WIDTH // 2,
                                       settings.GRID_HEIGHT // 2))
        self.food = Food.random_food(self.snake)
        self.running = True

        self.score = 0
        self.font = pygame.font.SysFont("Arial", 24)



    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.turn(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    self.snake.turn(Direction.DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake.turn(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake.turn(Direction.RIGHT)

    def update(self) -> None:
        # grow if food eaten
        grow = self.snake.head == self.food.position
        self.snake.move(grow=grow)

        if grow:
            self.food = Food.random_food(self.snake)
            self.score += 1 

        # check collisions
        if self.snake.check_self_collision() or self.snake.check_wall_collision(
            settings.GRID_WIDTH, settings.GRID_HEIGHT
        ):
            self.running = False

    def draw(self) -> None:
        self.screen.fill(settings.COLOR_BG)

        score_surface = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))

        # draw snake
        for segment in self.snake.body:
            pygame.draw.rect(
                self.screen,
                settings.COLOR_SNAKE,
                pygame.Rect(
                    segment.x * settings.CELL_SIZE,
                    segment.y * settings.CELL_SIZE,
                    settings.CELL_SIZE,
                    settings.CELL_SIZE,
                ),
            )

        # draw food
        pygame.draw.rect(
            self.screen,
            settings.COLOR_FOOD,
            pygame.Rect(
                self.food.position.x * settings.CELL_SIZE,
                self.food.position.y * settings.CELL_SIZE,
                settings.CELL_SIZE,
                settings.CELL_SIZE,
            ),
        )

        pygame.display.flip()

    def game_over(self) -> None:
        self.screen.fill(settings.COLOR_BG)
        game_over_surface = self.font.render("GAME OVER", True, (255, 0, 0))
        score_surface = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))

        self.screen.blit(game_over_surface, (settings.GRID_WIDTH * settings.CELL_SIZE // 2 - 60,
                                            settings.GRID_HEIGHT * settings.CELL_SIZE // 2 - 20))
        self.screen.blit(score_surface, (settings.GRID_WIDTH * settings.CELL_SIZE // 2 - 70,
                                        settings.GRID_HEIGHT * settings.CELL_SIZE // 2 + 20))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    waiting = False
                    self.running = False


    def run(self) -> None:
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(settings.FPS)

        self.game_over()
        pygame.quit()
        sys.exit()
