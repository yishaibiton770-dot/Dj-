from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .library import Song


@dataclass
class RemixRecipe:
    song_id: str
    style: str
    beat_pattern: List[str]
    ducking_amount: float
    overlays: List[Dict[str, float]]


class RemixBuilder:
    """Generate a lightweight beat overlay description that aligns to the beat grid."""

    DEFAULT_PATTERNS = {
        "house": ["kick", "hat", "kick", "snare"],
        "techno": ["kick", "kick", "hat", "clap"],
        "hiphop": ["kick", "snare", "kick", "snare"],
    }

    def build(self, song: Song, style: str = "house") -> RemixRecipe:
        pattern = self.DEFAULT_PATTERNS.get(style, self.DEFAULT_PATTERNS["house"])
        overlays: List[Dict[str, float]] = []
        for index, beat_time in enumerate(song.beat_grid[:32]):
            overlays.append({"time": beat_time, "sample": pattern[index % len(pattern)]})

        ducking_amount = 0.25 if song.energy_profile and max(song.energy_profile) > 0.8 else 0.1

        return RemixRecipe(
            song_id=song.id,
            style=style,
            beat_pattern=pattern,
            ducking_amount=ducking_amount,
            overlays=overlays,
        )
