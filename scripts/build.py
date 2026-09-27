"""Build, smoke-test and archive a standalone app on the current OS."""

import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tarfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    os.chdir(ROOT)
    env = os.environ.copy()
    env["PYINSTALLER_CONFIG_DIR"] = str(ROOT / "build" / "pyinstaller-cache")
    command = [sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean",
               "--windowed", "--onedir", "--name", "NeonSnake", "--noupx",
               "--add-data", "README.md:.",
               "--add-data", "THIRD_PARTY_NOTICES.md:.",
               "--osx-bundle-identifier", "com.overthetop.neonsnake", "run_game.py"]
    subprocess.run(command, check=True, env=env)
    system = platform.system().lower()
    machine = platform.machine().lower()
    arch = "arm64" if machine in ("arm64", "aarch64") else "x64"
    executable = ROOT / "dist" / "NeonSnake" / ("NeonSnake.exe" if system == "windows" else "NeonSnake")
    if system == "darwin":
        executable = ROOT / "dist" / "NeonSnake.app" / "Contents" / "MacOS" / "NeonSnake"
    smoke = ROOT / "artifacts" / f"packaged-{system}-{arch}"
    smoke.mkdir(parents=True, exist_ok=True)
    marker = smoke / "smoke-ok.txt"
    marker.unlink(missing_ok=True)
    smoke_env = env.copy()
    smoke_env.update(SDL_AUDIODRIVER="dummy", SDL_VIDEODRIVER="dummy")
    subprocess.run([str(executable), "--smoke-test", str(smoke)], check=True,
                   env=smoke_env, timeout=60)
    if not marker.exists():
        raise RuntimeError("Packaged app did not complete its smoke test")
    archives = ROOT / "dist" / "archives"
    archives.mkdir(exist_ok=True)
    name = f"NeonSnake-{system}-{arch}"
    if system == "darwin":
        destination = archives / f"{name}.zip"
        # ditto preserves the app bundle's executable permissions and symlinks.
        subprocess.run(["ditto", "-c", "-k", "--sequesterRsrc", "--keepParent",
                        str(ROOT / "dist" / "NeonSnake.app"), str(destination)], check=True)
    else:
        folder = ROOT / "dist" / "NeonSnake"
        shutil.copy2(ROOT / "README.md", folder / "README.md")
        shutil.copy2(ROOT / "THIRD_PARTY_NOTICES.md", folder / "THIRD_PARTY_NOTICES.md")
        if system == "windows":
            destination = archives / f"{name}.zip"
            with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
                for path in folder.rglob("*"):
                    if path.is_file():
                        archive.write(path, path.relative_to(folder.parent))
        else:
            destination = archives / f"{name}.tar.gz"
            with tarfile.open(destination, "w:gz") as archive:
                archive.add(folder, arcname="NeonSnake")
    print(f"Built and smoke-tested: {destination}")


if __name__ == "__main__":
    main()
