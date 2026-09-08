import sys
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from diagnostics import playback_mode_diagnosis, probe_media


class PlaybackDiagnosticsTests(unittest.TestCase):
    def test_missing_file_is_reported_without_ffprobe_execution(self):
        result = probe_media(ROOT_DIR / "tests" / "file_that_does_not_exist.mkv")
        self.assertFalse(result["exists"])
        self.assertEqual(result["error"], "Arquivo de mídia não encontrado.")

    def test_current_server_mode_is_direct_play(self):
        result = playback_mode_diagnosis({"error": None})
        self.assertEqual(result["mode"], "direct-play")
        self.assertEqual(result["source"], "original-media-file")
        self.assertFalse(result["transcoding"])


if __name__ == "__main__":
    unittest.main()
