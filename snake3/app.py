"""Desktop presentation and input for Neon Snake."""

import argparse
import math
import os
from pathlib import Path
import random
import tempfile

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame

from .audio import Audio
from .model import Direction, Game
from .storage import Store

WIDTH, HEIGHT = 1120, 800
BOARD = pygame.Rect(464, 144, 576, 576)
CELL = 24
BG = (10, 14, 23)
WHITE = (228, 237, 241)
MUTED = (135, 153, 168)
GREEN = (157, 255, 112)
TEAL = (68, 223, 182)
CORAL = (255, 132, 121)
KEYS = {pygame.K_UP: Direction.UP, pygame.K_w: Direction.UP,
        pygame.K_DOWN: Direction.DOWN, pygame.K_s: Direction.DOWN,
        pygame.K_LEFT: Direction.LEFT, pygame.K_a: Direction.LEFT,
        pygame.K_RIGHT: Direction.RIGHT, pygame.K_d: Direction.RIGHT}


class App:
    def __init__(self, save_path: Path | None = None, hidden: bool = False):
        pygame.display.init()
        pygame.font.init()
        self.hidden = hidden
        desktop = pygame.display.get_desktop_sizes()[0]
        scale = 1 if hidden else min(1, desktop[0] * 0.9 / WIDTH, desktop[1] * 0.9 / HEIGHT)
        initial_size = (round(WIDTH * scale), round(HEIGHT * scale))
        self.screen = pygame.display.set_mode(initial_size,
                                              pygame.HIDDEN if hidden else pygame.RESIZABLE)
        pygame.display.set_caption("Neon Snake")
        self.canvas = pygame.Surface((WIDTH, HEIGHT)).convert()
        self.fonts = {}
        self.text_cache = {}
        self.clock = pygame.time.Clock()
        self.store = Store(save_path)
        self.audio = Audio()
        self.audio.levels(self.store.prefs.music, self.store.prefs.effects, True)
        self.game = Game()
        self.state = "menu"
        self.settings = False
        self.selection = 0
        self.accumulator = 0.0
        self.countdown = 0.0
        self.elapsed = 0.0
        self.flash = 0.0
        self.particles = []
        self.buttons = []
        self.mouse = (-1, -1)
        self.focused = True
        self.running = True
        self.fullscreen = False
        self.window_size = initial_size
        self.run_best = self.store.prefs.best
        self.background = self.make_background()
        self.glow = self.make_glow(TEAL, 50)
        self.food_glow = self.make_glow(CORAL, 60)
        icon = pygame.Surface((64, 64))
        icon.fill(BG)
        pygame.draw.lines(icon, GREEN, False, [(15, 45), (40, 45), (40, 20), (20, 20)], 12)
        for p in [(15, 45), (40, 45), (40, 20), (20, 20)]:
            pygame.draw.circle(icon, GREEN, p, 6)
        pygame.draw.circle(icon, BG, (18, 18), 2)
        pygame.display.set_icon(icon)

    def text(self, value, x, y, size=24, color=WHITE, align="left"):
        value = str(value)
        key = (value, size, color)
        if key not in self.text_cache:
            font = self.fonts.setdefault(size, pygame.font.Font(None, size))
            if len(self.text_cache) > 400:
                self.text_cache.clear()
            self.text_cache[key] = font.render(value, True, color)
        surface = self.text_cache[key]
        rect = surface.get_rect(topleft=(x, y))
        if align == "center":
            rect.midtop = (x, y)
        elif align == "right":
            rect.topright = (x, y)
        self.canvas.blit(surface, rect)

    def label(self, value, x, y, color=MUTED):
        for letter in value:
            self.text(letter, x, y, 18, color)
            x += 11

    def make_background(self):
        surface = pygame.Surface((WIDTH, HEIGHT)).convert()
        surface.fill(BG)
        # A quiet green wash behind the board, generated once.
        for radius in range(490, 0, -5):
            amount = 1 - radius / 490
            color = (10, int(14 + 8 * amount), int(23 + 5 * amount))
            pygame.draw.circle(surface, color, (800, 380), radius)
        pygame.draw.rect(surface, (29, 47, 49), BOARD.inflate(8, 8), border_radius=12)
        pygame.draw.rect(surface, (13, 23, 30), BOARD, border_radius=8)
        for x in range(24):
            for y in range(24):
                pygame.draw.circle(surface, (33, 48, 53),
                                   (BOARD.x + x * CELL + 12, BOARD.y + y * CELL + 12), 1)
        return surface

    @staticmethod
    def make_glow(color, radius):
        surface = pygame.Surface((radius * 2, radius * 2)).convert()
        surface.fill((0, 0, 0))
        for r in range(radius, 0, -2):
            strength = (1 - r / radius) ** 2 * 0.17
            pygame.draw.circle(surface, tuple(int(c * strength) for c in color),
                               (radius, radius), r)
        return surface

    def button(self, rect, title, action, primary=False, selected=False):
        rect = pygame.Rect(rect)
        hover = rect.collidepoint(self.mouse) or selected
        fill = GREEN if primary else ((40, 58, 61) if hover else (23, 35, 43))
        if primary and hover:
            fill = (183, 255, 150)
        pygame.draw.rect(self.canvas, fill, rect, border_radius=9)
        if not primary:
            pygame.draw.rect(self.canvas, (65, 91, 88) if hover else (43, 60, 67),
                             rect, 1, border_radius=9)
        self.text(title, rect.centerx, rect.y + (rect.h - 22) // 2, 25,
                  BG if primary else WHITE, "center")
        self.buttons.append((rect, action))

    def start(self):
        self.game = Game()
        self.run_best = self.store.prefs.best
        self.accumulator = 0
        self.particles.clear()
        self.flash = 0
        self.state = "playing"
        self.settings = False
        self.audio.play("click")

    def pause(self):
        if self.state in ("playing", "countdown"):
            self.state = "paused"
            self.game.turns.clear()

    def resume(self):
        if self.focused:
            self.state = "countdown"
            self.countdown = 3.0
            self.settings = False

    def toggle_fullscreen(self):
        if self.hidden:
            return
        self.pause()
        if not self.fullscreen:
            self.window_size = self.screen.get_size()
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        self.fullscreen = not self.fullscreen

    def activate(self, action):
        if action == "start":
            self.start()
        elif action == "resume":
            self.resume()
        elif action == "pause":
            self.pause()
        elif action == "settings":
            self.pause()
            self.settings = not self.settings
            if not self.settings:
                self.store.save()
        elif action == "menu":
            self.state = "menu"
            self.settings = False
            self.game = Game()
            self.particles.clear()
        elif action == "fullscreen":
            self.toggle_fullscreen()
        elif action == "reduced":
            self.store.prefs.reduced = not self.store.prefs.reduced
            self.particles.clear()
            self.store.save()
        elif action.startswith(("music", "effects")):
            name, amount = action.split(":")
            value = getattr(self.store.prefs, name) + float(amount)
            setattr(self.store.prefs, name, round(max(0, min(1, value)), 2))
            self.store.save()

    def event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.WINDOWFOCUSLOST:
            self.focused = False
            self.pause()
        elif event.type == pygame.WINDOWFOCUSGAINED:
            self.focused = True
        elif event.type == pygame.KEYDOWN:
            if getattr(event, "repeat", False):
                return
            key = event.key
            if key == pygame.K_F11:
                self.toggle_fullscreen()
            elif key == pygame.K_ESCAPE:
                if self.settings:
                    self.settings = False
                    self.store.save()
                elif self.state in ("playing", "countdown"):
                    self.pause()
                elif self.state == "paused":
                    self.resume()
            elif key == pygame.K_TAB and not self.settings:
                self.activate("settings")
            elif self.settings:
                if key in (pygame.K_DOWN, pygame.K_s, pygame.K_TAB):
                    self.selection = (self.selection + 1) % 4
                elif key in (pygame.K_UP, pygame.K_w):
                    self.selection = (self.selection - 1) % 4
                elif key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN, pygame.K_SPACE):
                    if self.selection < 2:
                        name = ("music", "effects")[self.selection]
                        self.activate(f"{name}:{-0.1 if key == pygame.K_LEFT else 0.1}")
                    elif self.selection == 2:
                        self.activate("reduced")
                    else:
                        self.activate("settings")
            elif key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.state in ("menu", "over"):
                    self.start()
                elif self.state == "paused":
                    self.resume()
            elif key in KEYS and self.state in ("playing", "countdown"):
                self.game.turn(KEYS[key])
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            point = self.to_canvas(event.pos)
            for rect, action in reversed(self.buttons):
                if rect.collidepoint(point):
                    self.activate(action)
                    break

    def to_canvas(self, pos):
        w, h = self.screen.get_size()
        scale = min(w / WIDTH, h / HEIGHT)
        return ((pos[0] - (w - WIDTH * scale) / 2) / scale,
                (pos[1] - (h - HEIGHT * scale) / 2) / scale)

    def burst(self, cell):
        if self.store.prefs.reduced:
            return
        x = BOARD.x + (cell[0] + 0.5) * CELL
        y = BOARD.y + (cell[1] + 0.5) * CELL
        for _ in range(18):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(30, 130)
            self.particles.append([x, y, math.cos(angle) * speed,
                                   math.sin(angle) * speed, random.uniform(0.25, 0.55)])

    def update(self, dt):
        self.elapsed += dt
        self.flash = max(0, self.flash - dt)
        if self.state == "countdown":
            self.countdown -= dt
            if self.countdown <= 0:
                self.state = "playing"
            # Never apply countdown time to the simulation.
        elif self.state == "playing":
            self.accumulator += dt
            while self.accumulator >= 1 / self.game.speed:
                self.accumulator -= 1 / self.game.speed
                result = self.game.step()
                if result in ("eat", "win"):
                    self.burst(self.game.snake[0])
                    self.audio.play(result)
                    if self.game.score > self.store.prefs.best:
                        self.store.prefs.best = self.game.score
                        self.store.save()
                if result in ("collision", "win"):
                    if result == "collision":
                        self.audio.play("collision")
                    self.state = "over"
                    self.flash = 0.35
                    self.accumulator = 0
                    break
        if self.state not in ("paused", "countdown") and not self.settings:
            for p in self.particles:
                p[0] += p[2] * dt
                p[1] += p[3] * dt
                p[4] -= dt
            self.particles = [p for p in self.particles if p[4] > 0]
        self.audio.levels(self.store.prefs.music, self.store.prefs.effects,
                          self.state != "playing" or not self.focused)

    def draw_snake(self):
        if self.state == "menu":
            cells = [(14, 11), (13, 11), (12, 11), (11, 11), (10, 11),
                     (9, 11), (9, 12), (9, 13), (9, 14), (8, 14), (7, 14)]
            points = [(BOARD.x + (x + 0.5) * CELL, BOARD.y + (y + 0.5) * CELL)
                      for x, y in cells]
            direction = Direction.RIGHT
        else:
            blend = min(1, self.accumulator * self.game.speed)
            if self.state == "over":
                blend = 1
            points = []
            for i, (x, y) in enumerate(self.game.snake):
                px, py = self.game.previous[min(i, len(self.game.previous) - 1)]
                points.append((BOARD.x + (px + (x - px) * blend + 0.5) * CELL,
                               BOARD.y + (py + (y - py) * blend + 0.5) * CELL))
            direction = self.game.direction
        if not self.store.prefs.reduced:
            for x, y in points[::2]:
                self.canvas.blit(self.glow, (x - 50, y - 50), special_flags=pygame.BLEND_RGB_ADD)
        color = CORAL if self.state == "over" and not self.game.won else TEAL
        for i, p in reversed(list(enumerate(points))):
            t = 1 - i / len(points)
            shade = tuple(int(color[c] * (1 - t) + GREEN[c] * t) for c in range(3))
            if self.state == "over" and not self.game.won:
                shade = CORAL
            if i < len(points) - 1:
                pygame.draw.line(self.canvas, shade, p, points[i + 1], 17)
            pygame.draw.circle(self.canvas, shade, p, 9)
            if i > 0:
                pygame.draw.circle(self.canvas, (124, 218, 151), p, 2)
        head = points[0]
        dx, dy = direction.value
        for side in (-1, 1):
            eye = (head[0] + dx * 4 - dy * 4 * side,
                   head[1] + dy * 4 + dx * 4 * side)
            pygame.draw.circle(self.canvas, (15, 35, 30), eye, 2)

    def draw_board(self):
        self.canvas.set_clip(BOARD)
        food = (17, 8) if self.state == "menu" else self.game.food
        if food:
            x, y = BOARD.x + (food[0] + 0.5) * CELL, BOARD.y + (food[1] + 0.5) * CELL
            pulse = 0 if self.store.prefs.reduced else math.sin(self.elapsed * 3) * 1.5
            if not self.store.prefs.reduced:
                self.canvas.blit(self.food_glow, (x - 60, y - 60), special_flags=pygame.BLEND_RGB_ADD)
            pygame.draw.circle(self.canvas, (90, 55, 55), (x, y), 12 + pulse, 1)
            pygame.draw.circle(self.canvas, CORAL, (x, y), 6)
            pygame.draw.circle(self.canvas, (255, 222, 188), (x - 2, y - 2), 2)
        self.draw_snake()
        for x, y, _, _, life in self.particles:
            pygame.draw.circle(self.canvas, CORAL, (x, y), max(1, int(life * 6)))
        self.canvas.set_clip(None)
        if self.flash > 0 and not self.store.prefs.reduced:
            pygame.draw.rect(self.canvas, TEAL if self.game.won else CORAL,
                             BOARD.inflate(4, 4), 2, border_radius=10)

    def draw_settings(self):
        self.buttons.clear()
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((4, 9, 16, 225))
        self.canvas.blit(shade, (0, 0))
        rect = pygame.Rect(318, 146, 484, 502)
        pygame.draw.rect(self.canvas, (17, 28, 37), rect, border_radius=18)
        pygame.draw.rect(self.canvas, (51, 74, 77), rect, 1, border_radius=18)
        self.label("MAKE IT YOURS", 358, 183, TEAL)
        self.text("Settings", 358, 218, 48)
        for i, (name, title) in enumerate((("music", "Music"), ("effects", "Sound effects"))):
            y = 295 + i * 88
            value = getattr(self.store.prefs, name)
            self.text(title, 358, y, 26, GREEN if self.selection == i else WHITE)
            self.text(f"{round(value * 100)}%", 607, y, 24, MUTED, "right")
            pygame.draw.rect(self.canvas, (39, 57, 65), (358, y + 32, 245, 5), border_radius=2)
            if value:
                pygame.draw.rect(self.canvas, TEAL, (358, y + 32, round(245 * value), 5), border_radius=2)
            self.button((632, y - 5, 52, 44), "-", f"{name}:-0.1")
            self.button((698, y - 5, 52, 44), "+", f"{name}:0.1")
        self.text("Reduced effects", 358, 480, 26, GREEN if self.selection == 2 else WHITE)
        self.text("Less glow, no particles or pulsing", 358, 511, 20, MUTED)
        self.button((652, 476, 98, 42), "On" if self.store.prefs.reduced else "Off", "reduced")
        self.button((358, 558, 392, 48), "Done  /  ESC", "settings", True, self.selection == 3)
        self.text("Up / down to select  -  Left / right to adjust", WIDTH // 2, 672, 22, MUTED, "center")

    def draw(self):
        self.canvas.blit(self.background, (0, 0))
        self.buttons.clear()
        self.mouse = self.to_canvas(pygame.mouse.get_pos())
        pygame.draw.circle(self.canvas, GREEN, (71, 63), 6)
        self.label("NEON SNAKE", 91, 56, WHITE)
        self.text("A CLASSIC, IN A NEW LIGHT.", 1040, 56, 19, MUTED, "right")
        pygame.draw.line(self.canvas, (38, 51, 60), (64, 98), (1040, 98))
        self.label("ONE MORE BITE", 64, 157, TEAL)
        self.text("NEON", 60, 195, 94)
        self.text("SNAKE", 60, 269, 94, GREEN)
        self.text("Find your rhythm.", 65, 377, 30, WHITE)
        self.text("Chase your best.", 65, 411, 30, MUTED)
        self.label("PERSONAL BEST", 65, 476)
        self.text(f"{self.store.prefs.best:04}", 62, 504, 57)
        if self.state == "menu":
            self.button((64, 584, 304, 55), "Play  /  ENTER", "start", True)
        elif self.state in ("playing", "countdown"):
            self.button((64, 584, 304, 55), "Pause  /  ESC", "pause")
        elif self.state == "paused":
            self.button((64, 584, 304, 55), "Resume  /  ENTER", "resume", True)
        else:
            self.button((64, 584, 304, 55), "Play again  /  ENTER", "start", True)
        self.button((64, 652, 146, 43), "Settings", "settings")
        self.button((222, 652, 146, 43), "Fullscreen", "fullscreen")
        self.text("SCORE", BOARD.x, 113, 19, MUTED)
        self.text(f"{self.game.score:04}", BOARD.x + 64, 109, 30)
        self.text(f"{self.game.speed:g} CELLS / SEC", BOARD.right, 114, 18, TEAL, "right")
        self.draw_board()
        if self.state == "menu":
            self.label("24 x 24  /  ENDLESS FOCUS", 615, 220)
            self.text("Eat. Grow. Go again.", BOARD.centerx, 593, 34, WHITE, "center")
            self.text("Avoid the walls and your own body.", BOARD.centerx, 633, 24, MUTED, "center")
        elif self.state in ("paused", "countdown", "over"):
            veil = pygame.Surface(BOARD.size, pygame.SRCALPHA)
            veil.fill((8, 16, 24, 185))
            self.canvas.blit(veil, BOARD)
            cx = BOARD.centerx
            if self.state == "paused":
                self.label("TAKE A BREATHER", cx - 83, 316, TEAL)
                self.text("Paused", cx, 358, 68, WHITE, "center")
                self.text("Your run is right here.", cx, 434, 26, MUTED, "center")
                self.button((cx - 142, 497, 284, 52), "Resume  /  ENTER", "resume", True)
                self.button((cx - 142, 563, 284, 44), "Back to title", "menu")
            elif self.state == "countdown":
                self.text("Find your rhythm", cx, 330, 29, MUTED, "center")
                self.text(str(max(1, math.ceil(self.countdown))), cx, 380, 110, GREEN, "center")
            else:
                self.label("BOARD COMPLETE" if self.game.won else "EVERY RUN IS A FRESH START", cx - (77 if self.game.won else 132), 294, TEAL)
                self.text("You did it." if self.game.won else "Nice run.", cx, 334, 68, WHITE, "center")
                self.text(f"{self.game.score:04}", cx, 404, 70, GREEN, "center")
                self.text("NEW PERSONAL BEST" if self.game.score > self.run_best else "POINTS", cx, 477, 20, TEAL, "center")
                self.button((cx - 142, 524, 284, 52), "Play again  /  ENTER", "start", True)
        self.text("ARROWS / WASD   Move", 64, 752, 20, MUTED)
        self.text("ESC   Pause     TAB   Settings     F11   Fullscreen", 1040, 752, 20, MUTED, "right")
        if self.store.error:
            self.text(self.store.error, BOARD.centerx, 730, 19, CORAL, "center")
        elif not self.audio.available:
            self.text("Audio device unavailable - playing silently", BOARD.centerx, 730, 19, MUTED, "center")
        if self.settings:
            self.draw_settings()
        w, h = self.screen.get_size()
        scale = min(w / WIDTH, h / HEIGHT)
        size = (max(1, int(WIDTH * scale)), max(1, int(HEIGHT * scale)))
        self.screen.fill(BG)
        scaled = self.canvas if size == (WIDTH, HEIGHT) else pygame.transform.smoothscale(self.canvas, size)
        self.screen.blit(scaled, ((w - size[0]) // 2, (h - size[1]) // 2))
        pygame.display.flip()

    def run(self):
        try:
            while self.running:
                # Long stalls pause instead of killing the player via catch-up ticks.
                dt = self.clock.tick(120) / 1000
                if dt > 0.25:
                    self.pause()
                    dt = 0
                for event in pygame.event.get():
                    self.event(event)
                self.update(dt)
                self.draw()
        finally:
            self.store.save()
            pygame.quit()


def smoke_test(output: Path):
    """Exercise packaged rendering, audio and input without touching player saves."""
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as directory:
        app = App(Path(directory) / "settings.json", hidden=True)
        try:
            app.draw()
            pygame.image.save(app.canvas, str(output / "title.png"))
            app.event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
            assert app.state == "playing"
            app.game.food = (app.game.snake[0][0] + 1, app.game.snake[0][1])
            app.update(1 / 6)
            assert app.game.score == 10
            for _ in range(8):
                app.update(1 / 120)
            app.draw()
            pygame.image.save(app.canvas, str(output / "playing.png"))
            app.event(pygame.event.Event(pygame.WINDOWFOCUSLOST))
            assert app.state == "paused"
            head = app.game.snake[0]
            app.update(1)
            assert app.game.snake[0] == head
            app.draw()
            pygame.image.save(app.canvas, str(output / "paused.png"))
            app.event(pygame.event.Event(pygame.WINDOWFOCUSGAINED))
            app.event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
            assert app.state == "countdown"
            app.update(3.1)
            assert app.state == "playing"
            app.activate("settings")
            app.draw()
            pygame.image.save(app.canvas, str(output / "settings.png"))
            app.activate("settings")
            app.resume()
            app.update(3.1)
            for _ in range(160):
                app.update(1 / 60)
            assert app.state == "over"
            app.draw()
            pygame.image.save(app.canvas, str(output / "game-over.png"))
            app.start()
            assert app.game.score == 0 and app.store.prefs.best == 10
            assert Store(app.store.path).prefs.best == 10
            (output / "smoke-ok.txt").write_text("Rendering, input, audio initialization, pause, resume, collision, restart and save passed.\n", encoding="utf-8")
        finally:
            pygame.quit()


def main():
    parser = argparse.ArgumentParser(description="Neon Snake")
    parser.add_argument("--smoke-test", type=Path, metavar="OUTPUT_DIR")
    args = parser.parse_args()
    if args.smoke_test:
        smoke_test(args.smoke_test)
    else:
        App().run()
