import os
import json
from types import SimpleNamespace

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
import pytest

from snake3.app import App, BOARD, CELL, smoke_test
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


def test_frame_stall_pauses_without_catch_up(app, monkeypatch):
    app.start()
    head = app.game.snake[0]
    # Replace only time and the operating-system event queue; run the real loop.
    app.clock = SimpleNamespace(tick=lambda limit: 300)
    monkeypatch.setattr(pygame.event, "get", lambda: [pygame.event.Event(pygame.QUIT)])
    app.run()
    assert app.state == "paused"
    assert app.game.snake[0] == head and app.game.alive


def test_fullscreen_switch_pauses_and_restores_window(app):
    app.hidden = False  # Exercise the real transition using SDL's dummy display.
    original_size = app.screen.get_size()
    app.start()
    head = app.game.snake[0]
    key(app, pygame.K_F11)
    assert app.fullscreen and app.state == "paused"
    app.update(1)
    assert app.game.snake[0] == head
    app.draw()
    key(app, pygame.K_F11)
    assert not app.fullscreen and app.state == "paused"
    assert app.screen.get_size() == original_size


def test_focus_loss_during_countdown_requires_explicit_resume(app):
    app.start()
    key(app, pygame.K_ESCAPE)
    key(app, pygame.K_RETURN)
    app.update(1)
    head = app.game.snake[0]
    key(app, pygame.K_UP)
    app.event(pygame.event.Event(pygame.WINDOWFOCUSLOST))
    app.update(5)
    app.event(pygame.event.Event(pygame.WINDOWFOCUSGAINED))
    app.update(5)
    assert app.state == "paused" and app.game.snake[0] == head
    key(app, pygame.K_RETURN)
    app.update(2.9)
    assert app.state == "countdown" and app.game.snake[0] == head
    app.update(0.2)
    app.update(1 / 6)
    assert app.game.snake[0] == (head[0] + 1, head[1])


def test_audio_device_failure_still_allows_scoring(tmp_path, monkeypatch):
    def unavailable(*args, **kwargs):
        raise pygame.error("No audio device")

    monkeypatch.setattr(pygame.mixer, "init", unavailable)
    instance = App(tmp_path / "prefs.json", hidden=True)
    try:
        assert not instance.audio.available
        key(instance, pygame.K_RETURN)
        instance.game.food = (13, 12)
        instance.update(1 / 6)
        instance.draw()
        assert instance.state == "playing" and instance.game.score == 10
        instance.update(1 / 6)
        assert instance.game.snake[0] == (14, 12)
    finally:
        pygame.quit()


def test_recovered_preferences_allow_play_and_relaunch(tmp_path):
    path = tmp_path / "prefs.json"
    path.write_text(json.dumps({"music": 10**400, "effects": -10**400, "best": 120}))
    instance = App(path, hidden=True)
    try:
        key(instance, pygame.K_RETURN)
        instance.game.food = (13, 12)
        instance.update(1 / 6)
        assert instance.game.score == 10 and instance.state == "playing"
        instance.activate("music:-0.1")
        assert instance.store.prefs.best == 120
    finally:
        pygame.quit()
    reloaded = App(path, hidden=True)
    try:
        assert reloaded.store.prefs.music == 0.9
        assert reloaded.store.prefs.effects == 0 and reloaded.store.prefs.best == 120
    finally:
        pygame.quit()


def test_reduced_effects_removes_glow_and_pulse_without_changing_rules(app):
    app.draw()
    # Sample empty space near the title snake: glow changes, body pixels do not.
    halo = (BOARD.x + 14.5 * CELL, BOARD.y + 12.4 * CELL)
    normal_halo = app.canvas.get_at(halo)
    key(app, pygame.K_TAB)
    key(app, pygame.K_DOWN)
    key(app, pygame.K_DOWN)
    key(app, pygame.K_RETURN)
    key(app, pygame.K_ESCAPE)
    app.draw()
    assert sum(app.canvas.get_at(halo)[:3]) < sum(normal_halo[:3])
    food_region = pygame.Rect(BOARD.x + 16 * CELL, BOARD.y + 7 * CELL, 72, 72)
    before = pygame.image.tobytes(app.canvas.subsurface(food_region), "RGB")
    app.update(0.5)
    app.draw()
    assert pygame.image.tobytes(app.canvas.subsurface(food_region), "RGB") == before
    key(app, pygame.K_RETURN)
    app.game.food = (13, 12)
    app.update(1 / 6)
    assert app.game.snake[0] == (13, 12) and app.game.score == 10
    assert len(app.game.snake) == 5 and app.game.speed == 6
    # Move the next food away so any coral pixels here would be eat particles.
    app.game.food = (0, 0)
    app.update(0.05)
    app.draw()
    burst_region = pygame.Rect(BOARD.x + 11 * CELL, BOARD.y + 10 * CELL, 120, 120)
    pixels = app.canvas.subsurface(burst_region)
    assert not any(r > 80 and r > g * 1.3 and r > b * 1.3
                   for x in range(pixels.get_width()) for y in range(pixels.get_height())
                   for r, g, b, _ in [pixels.get_at((x, y))])


def test_full_board_win_scores_and_keyboard_restart_keeps_best(app):
    key(app, pygame.K_RETURN)
    path = [(x, y) for y in range(24)
            for x in (range(24) if y % 2 == 0 else range(23, -1, -1))]
    app.game.snake = path[1:]
    app.game.previous = app.game.snake.copy()
    app.game.direction = Direction.LEFT
    app.game.food = (0, 0)
    app.game.score = 5710
    app.update(1 / 12)
    assert app.state == "over" and app.game.won
    assert app.game.score == 5720 and app.store.prefs.best == 5720
    assert len(app.game.snake) == 576 and app.game.food is None
    app.draw()
    key(app, pygame.K_RETURN)
    assert app.state == "playing" and app.game.score == 0
    assert len(app.game.snake) == 4 and app.store.prefs.best == 5720


def test_smoke_produces_countdown_and_win_evidence(tmp_path):
    smoke_test(tmp_path)
    for name in ("countdown.png", "win.png", "reduced-effects.png"):
        assert (tmp_path / name).is_file()
    assert (tmp_path / "smoke-ok.txt").is_file()
