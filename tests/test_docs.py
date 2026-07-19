from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


class DocumentationTests(unittest.TestCase):
    def markdown_files(self) -> list[Path]:
        return sorted(ROOT.rglob("*.md"))

    def test_markdown_is_strict_utf8_without_nul_bytes(self) -> None:
        files = self.markdown_files()
        self.assertGreaterEqual(len(files), 5)
        for path in files:
            with self.subTest(path=path.relative_to(ROOT)):
                data = path.read_bytes()
                self.assertNotIn(b"\x00", data)
                data.decode("utf-8", errors="strict")

    def test_local_markdown_links_resolve_inside_repository(self) -> None:
        root = ROOT.resolve()
        for path in self.markdown_files():
            text = path.read_text(encoding="utf-8")
            for raw_target in MARKDOWN_LINK.findall(text):
                target = raw_target.strip().split("#", 1)[0]
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                resolved = (path.parent / target).resolve()
                with self.subTest(path=path.relative_to(ROOT), target=target):
                    self.assertTrue(resolved == root or root in resolved.parents)
                    self.assertTrue(resolved.exists())

    def test_readme_states_scope_and_evidence_boundaries(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("## Scope and safety boundary", readme)
        self.assertIn("## Evidence and limitations", readme)
        self.assertIn("synthetic scenarios", readme)
        self.assertIn("do not claim", readme)


if __name__ == "__main__":
    unittest.main()
