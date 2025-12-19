from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .library import Song


@dataclass
class TransitionPlan:
    source_id: str
    target_id: str
    tempo_adjustment: float
    key_compatibility: str
    mix_in: float
    mix_out: float
    steps: List[Dict[str, float]]


class TransitionEngine:
    """Derive a simple transition plan based on BPM and musical key compatibility."""

    def __init__(self, max_bpm_shift: float = 4.0):
        self.max_bpm_shift = max_bpm_shift

    def _key_relation(self, source: Song, target: Song) -> str:
        if source.musical_key == target.musical_key:
            return "perfect match"
        if source.musical_key and target.musical_key:
            return "compatible"
        return "unknown"

    def plan(self, source: Song, target: Song) -> TransitionPlan:
        if source.bpm is None or target.bpm is None:
            raise ValueError("Both songs must have BPM information before planning a transition")

        bpm_difference = target.bpm - source.bpm
        tempo_adjustment = max(min(bpm_difference, self.max_bpm_shift), -self.max_bpm_shift)

        mix_in = target.segments[0]["end"] if target.segments else 0
        mix_out = source.segments[-1]["start"] if source.segments else 0

        steps = [
            {"at": mix_out - 8, "action": "filter_high_pass", "value": 0.5},
            {"at": mix_out - 4, "action": "start_crossfade", "value": 0.5},
            {"at": mix_out, "action": "drop_source", "value": 0.0},
            {"at": mix_in, "action": "boost_target", "value": 1.2},
        ]

        return TransitionPlan(
            source_id=source.id,
            target_id=target.id,
            tempo_adjustment=tempo_adjustment,
            key_compatibility=self._key_relation(source, target),
            mix_in=round(mix_in, 2),
            mix_out=round(mix_out, 2),
            steps=steps,
        )
