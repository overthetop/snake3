"""Original procedural soundtrack and effects. No downloads or audio assets."""

from array import array
import math
import sys

import pygame

RATE = 22050
TAU = math.tau


def pcm(values):
    result = array("h", (int(max(-1, min(1, v)) * 32767) for v in values))
    if sys.byteorder != "little":
        result.byteswap()
    return result.tobytes()


def tone(frequencies: tuple[float, ...], length: float) -> bytes:
    def samples():
        for i in range(int(RATE * length)):
            t = i / RATE
            index = min(len(frequencies) - 1, int(t / length * len(frequencies)))
            envelope = min(t * 140, 1) * (1 - t / length) ** 2
            yield math.sin(TAU * frequencies[index] * t) * envelope * 0.4
    return pcm(samples())


def soundtrack() -> bytes:
    # Four bars at 100 BPM. Am7 / Fmaj7 / Cmaj7 / G: an original soft arpeggio.
    chords = [(220, 261.626, 329.628, 391.995),
              (174.614, 220, 261.626, 329.628),
              (130.813, 164.814, 195.998, 246.942),
              (195.998, 246.942, 293.665, 369.994)]
    duration = 9.6
    def samples():
        for i in range(round(RATE * duration)):
            t = i / RATE
            chord = chords[min(3, int(t / 2.4))]
            beat = t % 0.3
            note = chord[int(t / 0.3) % 4]
            env = min(beat / 0.018, 1) * math.exp(-beat * 12)
            arp = math.sin(TAU * note * 2 * beat) * env * 0.16
            bar = t % 2.4
            pad_env = min(bar / 0.15, (2.4 - bar) / 0.3, 1)
            pad = sum(math.sin(TAU * n * bar) for n in chord) * 0.018 * pad_env
            pulse = t % 0.6
            kick = math.sin(TAU * 55 * pulse) * math.exp(-pulse * 32) * 0.13
            yield arp + pad + kick
    return pcm(samples())


class Audio:
    def __init__(self):
        self.available = False
        self.sounds = {}
        self.music_channel = None
        try:
            pygame.mixer.init(RATE, -16, 1, 512)
            pygame.mixer.set_num_channels(8)
            pygame.mixer.set_reserved(1)
            self.sounds = {
                "eat": pygame.mixer.Sound(buffer=tone((659.25, 987.77), 0.16)),
                "collision": pygame.mixer.Sound(buffer=tone((146.83, 110, 65.41), 0.45)),
                "win": pygame.mixer.Sound(buffer=tone((523.25, 659.25, 783.99, 1046.5), 0.7)),
                "click": pygame.mixer.Sound(buffer=tone((440, 659.25), 0.08)),
            }
            self.music = pygame.mixer.Sound(buffer=soundtrack())
            self.music_channel = pygame.mixer.Channel(0)
            self.music_channel.play(self.music, loops=-1, fade_ms=800)
            self.available = True
        except pygame.error:
            # Play remains available on machines without an audio device.
            pass

    def levels(self, music: float, effects: float, quiet: bool = False):
        if self.available and self.music_channel is not None:
            self.music_channel.set_volume(music * (0.4 if quiet else 1))
            for sound in self.sounds.values():
                sound.set_volume(effects)

    def play(self, name: str):
        if self.available and name in self.sounds:
            self.sounds[name].play()
