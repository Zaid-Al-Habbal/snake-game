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
            (
                settings.GRID_WIDTH * settings.CELL_SIZE,
                settings.GRID_HEIGHT * settings.CELL_SIZE,
            )
        )
        pygame.display.set_caption("Snake Game")

        self.clock = pygame.time.Clock()
        self.snake = Snake(
            start=Point(settings.GRID_WIDTH // 2, settings.GRID_HEIGHT // 2)
        )
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

    def game_over(self) -> bool:
        """
        Show game over screen with a Restart button.
        Returns True if the player chose to restart, False to quit.
        """
        button_w, button_h = 160, 50
        button_rect = pygame.Rect(
            settings.GRID_WIDTH * settings.CELL_SIZE // 2 - button_w // 2,
            settings.GRID_HEIGHT * settings.CELL_SIZE // 2 + 40,
            button_w,
            button_h,
        )

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    # any key restarts
                    return True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_rect.collidepoint(event.pos):
                        return True

            self.screen.fill(settings.COLOR_BG)
            game_over_surface = self.font.render("GAME OVER", True, (255, 0, 0))
            score_surface = self.font.render(
                f"Final Score: {self.score}", True, (255, 255, 255)
            )
            restart_surface = self.font.render("Restart", True, (0, 0, 0))

            self.screen.blit(
                game_over_surface,
                (
                    settings.GRID_WIDTH * settings.CELL_SIZE // 2
                    - game_over_surface.get_width() // 2,
                    settings.GRID_HEIGHT * settings.CELL_SIZE // 2 - 60,
                ),
            )
            self.screen.blit(
                score_surface,
                (
                    settings.GRID_WIDTH * settings.CELL_SIZE // 2
                    - score_surface.get_width() // 2,
                    settings.GRID_HEIGHT * settings.CELL_SIZE // 2 - 20,
                ),
            )

            # draw button (hover effect)
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (200, 200, 200), button_rect)
            else:
                pygame.draw.rect(self.screen, (240, 240, 240), button_rect)

            self.screen.blit(
                restart_surface,
                (
                    button_rect.x
                    + button_rect.w // 2
                    - restart_surface.get_width() // 2,
                    button_rect.y
                    + button_rect.h // 2
                    - restart_surface.get_height() // 2,
                ),
            )

            pygame.display.flip()
            self.clock.tick(30)

    def reset(self) -> None:
        """Reset game state for a restart."""
        self.snake = Snake(
            start=Point(settings.GRID_WIDTH // 2, settings.GRID_HEIGHT // 2)
        )
        self.food = Food.random_food(self.snake)
        self.score = 0
        self.running = True

    def run(self) -> None:
        while True:
            while self.running:
                self.handle_input()
                self.update()
                self.draw()
                self.clock.tick(settings.FPS)

            # Show game over and get choice
            restart = self.game_over()
            if restart:
                self.reset()
                continue
            else:
                break

        pygame.quit()
        sys.exit()
