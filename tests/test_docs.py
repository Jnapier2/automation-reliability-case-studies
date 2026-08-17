from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SHOWCASE_DOCS = (
    ROOT / "docs" / "gpu-mining-readiness.md",
    ROOT / "docs" / "crypto-spread-bot-reliability.md",
    ROOT / "docs" / "prediction-market-data-quality.md",
    ROOT / "docs" / "local-network-guard-evidence.md",
)
SENSITIVE_PATTERNS = {
    "personal_windows_path": re.compile(r"[A-Za-z]:\\Users\\", re.IGNORECASE),
    "openai_key": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{16,}\b"),
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "slack_token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    "private_key_header": re.compile(
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    ),
    "operational_secret_assignment": re.compile(
        r"(?i)\b(?:api[_ -]?key|api[_ -]?secret|private[_ -]?key|wallet|pool|password|token)\b\s*[:=]\s*\S+"
    ),
    "raw_ipv4_address": re.compile(
        r"(?<![\d.])(?:25[0-5]|2[0-4]\d|1?\d?\d)"
        r"(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}(?![\d.])"
    ),
}


class DocumentationTests(unittest.TestCase):
    def markdown_files(self) -> list[Path]:
        return sorted(ROOT.rglob("*.md"))

    def test_markdown_is_strict_utf8_without_nul_bytes(self) -> None:
        files = self.markdown_files()
        self.assertGreaterEqual(len(files), 10)
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
        self.assertIn("## Sanitization method", readme)
        self.assertIn("## Evidence and limitations", readme)
        self.assertIn("synthetic scenarios", readme)
        self.assertIn("do not claim", readme)
        for path in SHOWCASE_DOCS:
            self.assertIn(f"docs/{path.name}", readme)

    def test_named_showcases_state_provenance_and_public_boundary(self) -> None:
        required_headings = (
            "## Evidence source",
            "## Showcase objective",
            "## Reliability invariants",
            "## Synthetic scenarios",
            "## Public boundary",
            "## Limitations",
        )
        for path in SHOWCASE_DOCS:
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertTrue(path.is_file())
                text = path.read_text(encoding="utf-8")
                for heading in required_headings:
                    self.assertIn(heading, text)
                self.assertIn("working/save-state", text)
                self.assertIn("synthetic", text.lower())
                self.assertRegex(text.lower(), r"\bcannot\b")

    def test_named_showcases_contain_no_sensitive_or_operational_residue(self) -> None:
        for path in SHOWCASE_DOCS:
            text = path.read_text(encoding="utf-8")
            for label, pattern in SENSITIVE_PATTERNS.items():
                with self.subTest(path=path.relative_to(ROOT), pattern=label):
                    self.assertIsNone(pattern.search(text))


if __name__ == "__main__":
    unittest.main()
