import sqlite3
from pathlib import Path

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".m4v", ".ts", ".webm"}


def scan_library(library_path: Path, database_path: Path, media_type: str | None = None) -> int:
    """Indexa uma localização concreta da biblioteca, recursivamente e remove entradas obsoletas."""
    library_path = Path(library_path)
    if not library_path.is_dir():
        return 0
    items = []
    current_paths = set()
    for file_path in library_path.rglob("*"):
        if not file_path.is_file() or file_path.suffix.lower() not in VIDEO_EXTENSIONS:
            continue
        try:
            stat = file_path.stat()
            resolved = str(file_path.resolve())
        except OSError:
            continue
        detected_type = media_type
        if detected_type is None:
            detected_type = "series" if any(part.casefold() == "series" for part in file_path.parts) else "movie"
        current_paths.add(resolved)
        items.append((file_path.stem, detected_type, resolved, stat.st_size, stat.st_mtime))
    with sqlite3.connect(database_path) as connection:
        connection.executemany(
            """INSERT INTO media_items (title, media_type, file_path, file_size, modified_at)
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(file_path) DO UPDATE SET
                 title=excluded.title, media_type=excluded.media_type,
                 file_size=excluded.file_size, modified_at=excluded.modified_at""",
            items,
        )
        prefix = str(library_path.resolve())
        rows = connection.execute("SELECT id, file_path FROM media_items WHERE file_path = ? OR file_path LIKE ?", (prefix, prefix + "\\%")).fetchall()
        stale_ids = [row[0] for row in rows if row[1] not in current_paths]
        if stale_ids:
            connection.executemany("DELETE FROM media_items WHERE id = ?", ((item_id,) for item_id in stale_ids))
        connection.commit()
    return len(items)
