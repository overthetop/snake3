import json

from snake3.storage import Store


def test_save_survives_restart(tmp_path):
    path = tmp_path / "nested" / "settings.json"
    store = Store(path)
    store.prefs.best = 130
    store.prefs.music = 0
    store.prefs.reduced = True
    assert store.save()
    reloaded = Store(path)
    assert reloaded.prefs.best == 130
    assert reloaded.prefs.music == 0
    assert reloaded.prefs.reduced is True
    assert not list(path.parent.glob("*.tmp"))


def test_corrupt_file_recovers(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text("{broken", encoding="utf-8")
    store = Store(path)
    assert store.prefs.best == 0 and store.error
    assert store.save()
    assert Store(path).error == ""


def test_untrusted_settings_are_validated(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text(json.dumps({"best": True, "music": 900, "effects": float("nan"),
                                "reduced": "false"}), encoding="utf-8")
    prefs = Store(path).prefs
    assert prefs.best == 0 and prefs.music == 1
    assert prefs.effects == 0.65 and not prefs.reduced


def test_unwritable_location_is_nonfatal(tmp_path):
    parent = tmp_path / "file"
    parent.write_text("not a directory")
    store = Store(parent / "save.json")
    assert not store.save()
    assert store.error
