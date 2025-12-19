from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from .remix_builder import RemixRecipe
from .transition_engine import TransitionPlan


@dataclass
class RenderResult:
    path: Path
    metadata: Dict[str, str]


class RenderEngine:
    """Persist transition/remix instructions as human-readable JSON files."""

    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def render_transition(self, plan: TransitionPlan) -> RenderResult:
        payload = {
            "source": plan.source_id,
            "target": plan.target_id,
            "tempo_adjustment": plan.tempo_adjustment,
            "key_compatibility": plan.key_compatibility,
            "mix_in": plan.mix_in,
            "mix_out": plan.mix_out,
            "steps": plan.steps,
        }
        path = self.output_dir / f"transition_{plan.source_id}_to_{plan.target_id}.json"
        path.write_text(json.dumps(payload, indent=2))
        return RenderResult(path=path, metadata={"type": "transition"})

    def render_remix(self, recipe: RemixRecipe) -> RenderResult:
        payload = {
            "song": recipe.song_id,
            "style": recipe.style,
            "beat_pattern": recipe.beat_pattern,
            "ducking_amount": recipe.ducking_amount,
            "overlays": recipe.overlays,
        }
        path = self.output_dir / f"remix_{recipe.song_id}.json"
        path.write_text(json.dumps(payload, indent=2))
        return RenderResult(path=path, metadata={"type": "remix"})
