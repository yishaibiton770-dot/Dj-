from pathlib import Path
import shutil
import unittest

from djai.audio_analysis import AudioAnalyzer
from djai.library import SongLibrary
from djai.remix_builder import RemixBuilder
from djai.render_engine import RenderEngine
from djai.transition_engine import TransitionEngine


class PipelineTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.base_dir = Path("demo_library")
        self.output_dir = Path("outputs")
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        if self.base_dir.exists():
            shutil.rmtree(self.base_dir)
        self.library = SongLibrary.demo_library(self.base_dir)

    def tearDown(self) -> None:
        shutil.rmtree(self.base_dir, ignore_errors=True)
        shutil.rmtree(self.output_dir, ignore_errors=True)

    def test_full_pipeline(self) -> None:
        analyzer = AudioAnalyzer()
        transition_engine = TransitionEngine()
        remix_builder = RemixBuilder()
        renderer = RenderEngine(self.output_dir)

        songs = list(self.library.songs())
        for song in songs:
            self.library.update_song(analyzer.annotate_song(song))

        plan = transition_engine.plan(songs[0], songs[1])
        remix = remix_builder.build(songs[0])

        transition_result = renderer.render_transition(plan)
        remix_result = renderer.render_remix(remix)

        self.assertTrue(transition_result.path.exists())
        self.assertTrue(remix_result.path.exists())
        self.assertTrue((self.output_dir / "library.json").exists() is False)


if __name__ == "__main__":
    unittest.main()
