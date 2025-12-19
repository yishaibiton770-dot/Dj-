from __future__ import annotations

import argparse
from pathlib import Path

from .audio_analysis import AudioAnalyzer
from .library import SongLibrary
from .remix_builder import RemixBuilder
from .render_engine import RenderEngine
from .transition_engine import TransitionEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Demo DJ AI pipeline")
    parser.add_argument("library", type=Path, help="Folder containing audio files")
    parser.add_argument("output", type=Path, help="Folder to store rendered plans")
    parser.add_argument("--style", default="house", help="Beat style for remix overlays")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    library = SongLibrary(args.library)
    library.scan()

    analyzer = AudioAnalyzer()
    transition_engine = TransitionEngine()
    remix_builder = RemixBuilder()
    renderer = RenderEngine(args.output)

    songs = list(library.songs())
    for song in songs:
        library.update_song(analyzer.annotate_song(song))

    if len(songs) >= 2:
        plan = transition_engine.plan(songs[0], songs[1])
        renderer.render_transition(plan)
    for song in songs:
        recipe = remix_builder.build(song, style=args.style)
        renderer.render_remix(recipe)

    library.save(args.output / "library.json")
    print(f"Analyzed {len(songs)} song(s). Plans saved to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
