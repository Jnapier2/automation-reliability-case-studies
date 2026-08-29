from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SHOWCASE_PROVENANCE = {
    ROOT / "docs" / "authorized-media-transfer-resilience.md": ("working/save-state",),
    ROOT / "docs" / "data-contract-monitor-governance.md": (
        "current public source authority",
        "data contract monitor v0.1.5",
        "private field rollback",
        "v0.1.2 user-confirmed windows working/save-state",
    ),
    ROOT / "docs" / "data-governance-lineage-portal.md": (
        "verified maintenance known-good",
    ),
    ROOT / "docs" / "gpu-mining-readiness.md": ("working/save-state",),
    ROOT / "docs" / "crypto-spread-bot-reliability.md": ("working/save-state",),
    ROOT / "docs" / "prediction-market-data-quality.md": ("working/save-state",),
    ROOT / "docs" / "prediction-market-save-state-reconciliation.md": ("working/save-state",),
    ROOT / "docs" / "prediction-market-structural-parity.md": (
        "folder-declared working save state",
    ),
    ROOT / "docs" / "local-network-guard-evidence.md": ("working/save-state",),
    ROOT / "docs" / "windows-repair-remediation-governance.md": (
        "working/save-state",
    ),
    ROOT / "docs" / "release-acceptance-fail-closed.md": (
        "save-state candidate",
        "failed closed",
    ),
}
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
    "private_drive_url": re.compile(
        r"https://(?:drive|docs)\.google\.com/", re.IGNORECASE
    ),
    "private_digest": re.compile(r"\b[a-fA-F0-9]{64}\b"),
}


class DocumentationTests(unittest.TestCase):
    def markdown_files(self) -> list[Path]:
        return sorted(ROOT.rglob("*.md"))

    def test_markdown_is_strict_utf8_without_nul_bytes(self) -> None:
        files = self.markdown_files()
        self.assertGreaterEqual(len(files), 17)
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
        self.assertIn("Thirteen engineering analyses", readme)
        self.assertIn("Eleven named showcase studies", readme)
        self.assertIn("## Professional Portfolio programs", readme)
        self.assertIn("docs/professional-portfolio-programs.md", readme)
        self.assertIn("## Scope and safety boundary", readme)
        self.assertIn("## Sanitization method", readme)
        self.assertIn("## Evidence and limitations", readme)
        self.assertIn("synthetic scenarios", readme)
        self.assertIn("do not claim", readme)
        for path in SHOWCASE_PROVENANCE:
            self.assertIn(f"docs/{path.name}", readme)

    def test_professional_portfolio_overview_tracks_all_programs(self) -> None:
        text = (
            ROOT / "docs" / "professional-portfolio-programs.md"
        ).read_text(encoding="utf-8").lower()
        required = (
            "data contract monitor",
            "data governance & lineage portal",
            "workflow and case management platform",
            "policy and procedure navigator",
            "pc reliability & incident intelligence suite",
            "operations intelligence & automation platform",
            "published studies",
            "reviewed and deferred programs",
            "current public source authority",
            "data contract monitor v0.1.5",
            "private field rollback",
            "v0.1.2 user-confirmed windows working/save-state",
            "public boundary",
        )
        for marker in required:
            self.assertIn(marker, text)

    def test_media_restart_reconciles_the_published_destination(self) -> None:
        raw = (
            ROOT / "docs" / "authorized-media-transfer-resilience.md"
        ).read_text(encoding="utf-8").lower()
        text = " ".join(raw.split())
        required = (
            "deterministic destination identity",
            "durable publication receipt",
            "before relaunching another worker",
            "destination and receipt already agree",
            "at most one published result",
            "retry budget exhausted",
            "budget expires with no prior publication",
            "ownership or publication state is ambiguous",
        )
        for marker in required:
            self.assertIn(marker, text)

    def test_named_showcases_state_provenance_and_public_boundary(self) -> None:
        required_headings = (
            "## Evidence source",
            "## Showcase objective",
            "## Reliability invariants",
            "## Synthetic scenarios",
            "## Public boundary",
            "## Limitations",
        )
        for path, provenance_markers in SHOWCASE_PROVENANCE.items():
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertTrue(path.is_file())
                text = path.read_text(encoding="utf-8")
                lower = text.lower()
                for heading in required_headings:
                    self.assertIn(heading, text)
                for marker in provenance_markers:
                    self.assertIn(marker, lower)
                self.assertIn("synthetic", lower)
                self.assertRegex(lower, r"\bcannot\b")

    def test_named_showcases_contain_no_sensitive_or_operational_residue(self) -> None:
        for path in SHOWCASE_PROVENANCE:
            text = path.read_text(encoding="utf-8")
            for label, pattern in SENSITIVE_PATTERNS.items():
                with self.subTest(path=path.relative_to(ROOT), pattern=label):
                    self.assertIsNone(pattern.search(text))


if __name__ == "__main__":
    unittest.main()
