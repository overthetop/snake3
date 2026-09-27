# Third-party components

The game uses pygame-ce (LGPL-2.1-or-later) and its SDL libraries, and standalone downloads bundle the Python runtime (PSF license). pygame-ce's default font is bundled with the dependency. Their upstream license files should be retained when distributing binaries.

- pygame-ce: https://github.com/pygame-community/pygame-ce
- Python: https://docs.python.org/3/license.html
- SDL: https://www.libsdl.org/license.php
- PyInstaller's bootloader exception permits distribution of bundled applications: https://pyinstaller.org/en/stable/license.html

The game's shapes are drawn by its own code. Music and sound effects are original procedural synthesis in `snake3/audio.py`; no third-party music, artwork, or downloaded fonts are used.
