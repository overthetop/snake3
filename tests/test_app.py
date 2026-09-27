import os

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
import pytest

from snake3.app import App
from snake3.model import Direction


@pytest.fixture
def app(tmp_path):
    instance = App(tmp_path / "prefs.json", hidden=True)
    yield instance
    pygame.quit()


def key(app, code):
    app.event(pygame.event.Event(pygame.KEYDOWN, key=code))


def test_pause_freezes_and_resume_does_not_catch_up(app):
    app.start()
    app.update(0.1)
    app.game.turn(Direction.UP)
    head = app.game.snake[0]
    app.event(pygame.event.Event(pygame.WINDOWFOCUSLOST))
    assert app.state == "paused" and not app.game.turns
    app.update(100)
    key(app, pygame.K_RETURN)
    assert app.state == "paused"  # Cannot resume without focus.
    app.event(pygame.event.Event(pygame.WINDOWFOCUSGAINED))
    key(app, pygame.K_RETURN)
    assert app.state == "countdown"
    app.update(3.2)
    assert app.game.snake[0] == head and app.state == "playing"
    app.update(0.07)
    assert app.game.snake[0] == (head[0] + 1, head[1])


def test_turn_buffer_runs_through_real_keyboard_events(app):
    app.start()
    key(app, pygame.K_UP)
    key(app, pygame.K_LEFT)
    app.update(1 / 6)
    app.update(1 / 6)
    assert app.game.snake[0] == (11, 11)


def test_settings_pause_and_keyboard_adjustments_persist(app):
    app.start()
    key(app, pygame.K_TAB)
    assert app.settings and app.state == "paused"
    key(app, pygame.K_LEFT)
    assert app.store.prefs.music == 0.08
    key(app, pygame.K_DOWN)
    key(app, pygame.K_DOWN)
    key(app, pygame.K_RETURN)
    assert app.store.prefs.reduced
    key(app, pygame.K_ESCAPE)
    assert not app.settings and app.state == "paused"


def test_render_all_states_and_letterboxing(app):
    for state in ("menu", "playing", "paused", "countdown", "over"):
        app.state = state
        app.draw()
    app.settings = True
    app.draw()
    app.screen = pygame.display.set_mode((800, 800), pygame.HIDDEN)
    app.draw()
    x, y = app.to_canvas((400, 400))
    assert x == pytest.approx(560) and y == pytest.approx(400)
