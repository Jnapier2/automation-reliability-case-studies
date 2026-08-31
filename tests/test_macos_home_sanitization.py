from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MACOS_HOME_PATH = re.compile(r"/Users/[A-Za-z0-9._-]+", re.IGNORECASE)
SHOWCASE_PATHS = (
    ROOT / "docs" / "authorized-media-transfer-resilience.md",
    ROOT / "docs" / "media-tagger-one-active-launcher.md",
    ROOT / "docs" / "gpu-mining-readiness.md",
    ROOT / "docs" / "crypto-spread-bot-reliability.md",
    ROOT / "docs" / "prediction-market-data-quality.md",
    ROOT / "docs" / "prediction-market-save-state-reconciliation.md",
    ROOT / "docs" / "prediction-market-structural-parity.md",
    ROOT / "docs" / "local-network-guard-evidence.md",
    ROOT / "docs" / "windows-repair-remediation-governance.md",
    ROOT / "docs" / "release-acceptance-fail-closed.md",
)


class MacOSHomeSanitizationTests(unittest.TestCase):
    def test_detector_matches_common_macos_home_path(self) -> None:
        self.assertIsNotNone(
            MACOS_HOME_PATH.search("/Users/example-user/private-project")
        )

    def test_named_showcases_contain_no_macos_home_paths(self) -> None:
        for path in SHOWCASE_PATHS:
            with self.subTest(path=path.relative_to(ROOT)):
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(MACOS_HOME_PATH.search(text))


if __name__ == "__main__":
    unittest.main()
