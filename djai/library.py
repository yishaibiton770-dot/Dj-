from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional


@dataclass
class Song:
    """Represents a track in the local library."""

    id: str
    title: str
    artist: str
    path: Path
    bpm: Optional[float] = None
    musical_key: Optional[str] = None
    duration_seconds: Optional[float] = None
    energy_profile: List[float] = field(default_factory=list)
    beat_grid: List[float] = field(default_factory=list)
    segments: List[Dict[str, float]] = field(default_factory=list)

    @property
    def display_name(self) -> str:
        return f"{self.artist} - {self.title}"


class SongLibrary:
    """A minimal library that indexes songs in a folder."""

    SUPPORTED_EXTENSIONS = {".mp3", ".wav", ".flac", ".ogg", ".txt"}

    def __init__(self, root: Path):
        self.root = Path(root)
        self._songs: Dict[str, Song] = {}

    def scan(self) -> None:
        """Discover songs inside the root directory and register metadata placeholders."""
        if not self.root.exists():
            raise FileNotFoundError(f"Library root {self.root} not found")

        for path in self.root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue

            song_id = path.stem
            if song_id in self._songs:
                continue

            title = path.stem.replace("_", " ")
            self._songs[song_id] = Song(
                id=song_id,
                title=title,
                artist="Unknown",
                path=path,
            )

    def songs(self) -> Iterable[Song]:
        return self._songs.values()

    def get(self, song_id: str) -> Optional[Song]:
        return self._songs.get(song_id)

    def update_song(self, updated: Song) -> None:
        self._songs[updated.id] = updated

    def to_json(self) -> str:
        return json.dumps({song.id: asdict(song) for song in self._songs.values()}, indent=2)

    def save(self, path: Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.to_json())

    @classmethod
    def load(cls, path: Path) -> "SongLibrary":
        data = json.loads(Path(path).read_text())
        library = cls(root=Path("."))
        for song_id, payload in data.items():
            library._songs[song_id] = Song(
                id=song_id,
                title=payload.get("title", song_id),
                artist=payload.get("artist", "Unknown"),
                path=Path(payload.get("path", song_id)),
                bpm=payload.get("bpm"),
                musical_key=payload.get("musical_key"),
                duration_seconds=payload.get("duration_seconds"),
                energy_profile=payload.get("energy_profile", []),
                beat_grid=payload.get("beat_grid", []),
                segments=payload.get("segments", []),
            )
        return library

    @staticmethod
    def demo_library(target: Path) -> "SongLibrary":
        """Create a tiny demo library with placeholder tracks."""
        target = Path(target)
        target.mkdir(parents=True, exist_ok=True)

        for index in range(1, 4):
            dummy_track = target / f"track_{index}.txt"
            if not dummy_track.exists():
                dummy_track.write_text("placeholder audio")

        library = SongLibrary(target)
        library.scan()
        return library
