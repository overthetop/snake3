"""Small, validated per-user save file; never write alongside the executable."""

from dataclasses import asdict, dataclass
import json
import math
import os
from pathlib import Path
import sys
import tempfile


def default_path() -> Path:
    if sys.platform == "win32":
        root = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local"))
    elif sys.platform == "darwin":
        root = Path.home() / "Library/Application Support"
    else:
        root = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share"))
    return root / "NeonSnake" / "settings.json"


@dataclass
class Preferences:
    best: int = 0
    music: float = 0.18
    effects: float = 0.65
    reduced: bool = False


class Store:
    def __init__(self, path: Path | None = None):
        self.path = path if path is not None else default_path()
        self.prefs = Preferences()
        self.error = ""
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(raw, dict):
                raise ValueError("Invalid save")
            best = raw.get("best", 0)
            if type(best) is int and 0 <= best <= 5720:
                self.prefs.best = best
            for key in ("music", "effects"):
                value = raw.get(key)
                if type(value) in (float, int) and math.isfinite(value):
                    setattr(self.prefs, key, max(0.0, min(1.0, value)))
            if type(raw.get("reduced")) is bool:
                self.prefs.reduced = raw["reduced"]
        except FileNotFoundError:
            pass
        except (OSError, ValueError, UnicodeError):
            self.error = "Could not read saved preferences. Using defaults."

    def save(self) -> bool:
        temporary = None
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=self.path.parent,
                                             delete=False, suffix=".tmp") as handle:
                temporary = Path(handle.name)
                json.dump(asdict(self.prefs), handle, indent=2)
            os.replace(temporary, self.path)
            self.error = ""
            return True
        except OSError:
            self.error = "Progress cannot be saved in this location."
            return False
        finally:
            if temporary is not None:
                try:
                    temporary.unlink(missing_ok=True)
                except OSError:
                    pass
