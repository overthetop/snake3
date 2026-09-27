import random

import pytest

from snake3.model import Direction, Game


def test_food_grows_and_scores_without_moving_tail():
    game = Game(rng=random.Random(1))
    tail = game.snake[-1]
    game.food = (13, 12)
    assert game.step() == "eat"
    assert len(game.snake) == 5 and game.snake[-1] == tail
    assert game.score == 10 and game.food not in game.snake


def test_fast_double_turn_is_preserved_and_reversal_rejected():
    game = Game()
    game.food = (0, 0)
    assert not game.turn(Direction.LEFT)
    assert game.turn(Direction.UP)
    assert not game.turn(Direction.DOWN)
    assert not game.turn(Direction.UP)
    assert game.turn(Direction.LEFT)
    assert not game.turn(Direction.DOWN)  # Queue is full.
    game.step()
    assert game.snake[0] == (12, 11)
    game.step()
    assert game.snake[0] == (11, 11)


def test_moving_into_vacating_tail_is_legal():
    game = Game()
    game.snake = [(2, 2), (2, 3), (1, 3), (1, 2)]
    game.direction = Direction.UP
    game.food = (10, 10)
    game.turn(Direction.LEFT)
    assert game.step() == "move"
    assert game.snake[0] == (1, 2) and game.alive


def test_self_collision_leaves_board_unchanged():
    game = Game()
    game.snake = [(2, 2), (2, 3), (1, 3), (1, 2), (1, 1)]
    game.direction = Direction.UP
    game.food = (10, 10)
    before = game.snake.copy()
    game.turn(Direction.LEFT)
    assert game.step() == "collision"
    assert not game.alive and game.snake == before
    assert game.step() == "idle"


@pytest.mark.parametrize("head,direction", [((0, 3), Direction.LEFT),
    ((23, 3), Direction.RIGHT), ((3, 0), Direction.UP), ((3, 23), Direction.DOWN)])
def test_all_walls_are_lethal(head, direction):
    game = Game()
    game.snake = [head]
    game.direction = direction
    assert game.step() == "collision"


def test_speed_thresholds_and_cap():
    game = Game()
    for score, expected in [(0, 6), (40, 6), (50, 6.5), (599, 11.5), (600, 12), (5720, 12)]:
        game.score = score
        assert game.speed == expected


def test_last_food_wins_without_random_choice_on_empty_board():
    game = Game(size=4)
    # A contiguous snake with only the next head cell unoccupied.
    game.snake = [(2, 0), (1, 0), (0, 0), (0, 1), (1, 1), (2, 1),
                  (3, 1), (3, 2), (2, 2), (1, 2), (0, 2), (0, 3),
                  (1, 3), (2, 3), (3, 3)]
    game.food = (3, 0)
    game.direction = Direction.RIGHT
    assert game.step() == "win"
    assert game.won and not game.alive and game.food is None
    assert len(game.snake) == 16


def test_food_uses_only_remaining_free_cell():
    game = Game(4)
    game.snake = [(x, y) for y in range(4) for x in range(4) if (x, y) != (3, 3)]
    assert game.spawn_food() == (3, 3)
