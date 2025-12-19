from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from .library import Song


@dataclass
class AnalysisResult:
    bpm: float
    musical_key: str
    duration_seconds: float
    energy_profile: List[float]
    beat_grid: List[float]
    segments: List[Dict[str, float]]


class AudioAnalyzer:
    """Fake-but-consistent audio analyzer that derives values from file content."""

    KEYS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    def __init__(self, default_duration: float = 180.0):
        self.default_duration = default_duration

    @staticmethod
    def _stable_hash(path: Path) -> int:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        return int(digest[:8], 16)

    def _estimate_bpm(self, seed: int) -> float:
        return 90 + (seed % 80)

    def _estimate_key(self, seed: int) -> str:
        return self.KEYS[seed % len(self.KEYS)]

    def _energy_profile(self, duration: float, seed: int) -> List[float]:
        buckets = int(duration // 10)
        profile = []
        for index in range(buckets):
            phase = (seed + index * 37) % 100 / 100
            energy = 0.4 + 0.6 * math.sin(phase * math.pi)
            profile.append(round(energy, 3))
        return profile or [0.5]

    def _beat_grid(self, bpm: float, duration: float) -> List[float]:
        if bpm <= 0:
            return []
        beat_interval = 60.0 / bpm
        beats = []
        position = 0.0
        while position < duration:
            beats.append(round(position, 3))
            position += beat_interval
        return beats

    def _segments(self, duration: float) -> List[Dict[str, float]]:
        step = duration / 4
        return [
            {"label": "intro", "start": 0, "end": step},
            {"label": "build", "start": step, "end": 2 * step},
            {"label": "drop", "start": 2 * step, "end": 3 * step},
            {"label": "outro", "start": 3 * step, "end": duration},
        ]

    def analyze(self, song: Song) -> AnalysisResult:
        seed = self._stable_hash(song.path)
        bpm = float(self._estimate_bpm(seed))
        musical_key = self._estimate_key(seed)
        duration = self.default_duration
        energy_profile = self._energy_profile(duration, seed)
        beat_grid = self._beat_grid(bpm, duration)
        segments = self._segments(duration)
        return AnalysisResult(
            bpm=bpm,
            musical_key=musical_key,
            duration_seconds=duration,
            energy_profile=energy_profile,
            beat_grid=beat_grid,
            segments=segments,
        )

    def annotate_song(self, song: Song) -> Song:
        result = self.analyze(song)
        song.bpm = result.bpm
        song.musical_key = result.musical_key
        song.duration_seconds = result.duration_seconds
        song.energy_profile = result.energy_profile
        song.beat_grid = result.beat_grid
        song.segments = result.segments
        return song
