import sqlite3
from pathlib import Path

from scanner import scan_library


def prepare_db(path: Path):
    with sqlite3.connect(path) as c:
        c.execute("CREATE TABLE media_items (id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,media_type TEXT NOT NULL,file_path TEXT NOT NULL UNIQUE,file_size INTEGER,modified_at TEXT)")
        c.commit()


def test_scan_library_uses_registered_path_directly_and_refreshes_stale_entries(tmp_path):
    root = tmp_path / "Midia" / "Filmes"
    root.mkdir(parents=True)
    video = root / "Filme A.mp4"
    video.write_bytes(b"video")
    db = tmp_path / "library.db"
    prepare_db(db)

    assert scan_library(root, db) == 1
    with sqlite3.connect(db) as c:
        rows = c.execute("SELECT title, media_type, file_path FROM media_items").fetchall()
    assert rows[0][0] == "Filme A"
    assert rows[0][1] == "movie"
    assert rows[0][2] == str(video.resolve())

    video.unlink()
    assert scan_library(root, db) == 0
    with sqlite3.connect(db) as c:
        assert c.execute("SELECT COUNT(*) FROM media_items").fetchone()[0] == 0


def test_scan_library_detects_series_from_registered_path(tmp_path):
    root = tmp_path / "Midia" / "Series" / "Temporada 1"
    root.mkdir(parents=True)
    (root / "Episodio 01.mkv").write_bytes(b"video")
    db = tmp_path / "library.db"
    prepare_db(db)

    assert scan_library(root, db) == 1
    with sqlite3.connect(db) as c:
        assert c.execute("SELECT media_type FROM media_items").fetchone()[0] == "series"
