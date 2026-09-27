"""Shared, deterministic game scenarios for tests and packaged validation."""

from .model import Direction, Game


def almost_full_board() -> Game:
    """Return a contiguous 24-by-24 snake one normal move away from winning."""
    game = Game()
    path = [(x, y) for y in range(24)
            for x in (range(24) if y % 2 == 0 else range(23, -1, -1))]
    game.snake = path[1:]
    game.previous = game.snake.copy()
    game.direction = Direction.LEFT
    game.food = (0, 0)
    game.score = 5710
    return game
