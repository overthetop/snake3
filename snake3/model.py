"""Deterministic grid rules, with no dependency on the renderer or clock."""

from collections import deque
from enum import Enum
import random

Cell = tuple[int, int]


class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    def opposite(self, other: "Direction") -> bool:
        return self.value == (-other.value[0], -other.value[1])


class Game:
    def __init__(self, size: int = 24, rng: random.Random | None = None):
        if size < 4:
            raise ValueError("Board must be at least four cells wide")
        self.size = size
        self.rng = rng or random.Random()
        x, y = max(3, size // 2), size // 2
        self.snake: list[Cell] = [(x - i, y) for i in range(4)]
        self.previous = self.snake.copy()
        self.direction = Direction.RIGHT
        self.turns: deque[Direction] = deque()
        self.score = 0
        self.alive = True
        self.won = False
        self.food: Cell | None = self.spawn_food()

    @property
    def speed(self) -> float:
        return min(12.0, 6.0 + (self.score // 50) * 0.5)

    def spawn_food(self) -> Cell | None:
        occupied = set(self.snake)
        free = [(x, y) for y in range(self.size) for x in range(self.size)
                if (x, y) not in occupied]
        return self.rng.choice(free) if free else None

    def turn(self, direction: Direction) -> bool:
        """Buffer at most two intentional turns; reject repeats and reversals."""
        if not self.alive or len(self.turns) >= 2:
            return False
        last = self.turns[-1] if self.turns else self.direction
        if direction == last or direction.opposite(last):
            return False
        self.turns.append(direction)
        return True

    def step(self) -> str:
        if not self.alive:
            return "idle"
        if self.turns:
            self.direction = self.turns.popleft()
        dx, dy = self.direction.value
        head = (self.snake[0][0] + dx, self.snake[0][1] + dy)
        growing = head == self.food
        # Moving into the tail's current cell is legal when it vacates it.
        body = self.snake if growing else self.snake[:-1]
        if not (0 <= head[0] < self.size and 0 <= head[1] < self.size) or head in body:
            self.alive = False
            self.turns.clear()
            return "collision"
        self.previous = self.snake.copy()
        self.snake.insert(0, head)
        if not growing:
            self.snake.pop()
            return "move"
        self.score += 10
        self.food = self.spawn_food()
        if self.food is None:
            self.won = True
            self.alive = False
            return "win"
        return "eat"
