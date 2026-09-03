from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
BACKSLASH = chr(92)
PRIVATE_KEY_MARKER = "-" * 5 + "BEGIN PRIVATE KEY" + "-" * 5
SHOWCASE_PROVENANCE = {
    ROOT / "docs" / "authorized-media-transfer-resilience.md": ("working/save-state",),
    ROOT / "docs" / "media-tagger-one-active-launcher.md": (
        "release candidate",
        "v0.5.16 source baseline",
    ),
    ROOT / "docs" / "botops-control-plane-cohesion.md": (
        "windows scan-accepted foundation save state",
        "confirmed control rollback",
    ),
    ROOT / "docs" / "gpu-mining-readiness.md": ("working/save-state",),
    ROOT / "docs" / "crypto-spread-bot-reliability.md": ("working/save-state",),
    ROOT / "docs" / "prediction-market-data-quality.md": ("working/save-state",),
    ROOT / "docs" / "prediction-market-save-state-reconciliation.md": ("working/save-state",),
    ROOT / "docs" / "prediction-market-structural-parity.md": (
        "folder-declared working save state",
    ),
    ROOT / "docs" / "local-network-guard-evidence.md": ("working/save-state",),
    ROOT / "docs" / "gateway-intelligence-core-evidence.md": (
        "exact-archive-qualified windows test candidate",
        "v0.1.3 as its rollback",
    ),
    ROOT / "docs" / "windows-repair-remediation-governance.md": (
        "consolidation candidate",
        "accepted v55.29.4 working baseline",
    ),
    ROOT / "docs" / "release-acceptance-fail-closed.md": (
        "save-state candidate",
        "failed closed",
    ),
}
SENSITIVE_PATTERNS = {
    "personal_windows_path": re.compile(
        r"[A-Za-z]:" + re.escape(BACKSLASH) + r"Users" + re.escape(BACKSLASH),
        re.IGNORECASE,
    ),
    "unix_home_path": re.compile(r"/home/[A-Za-z0-9._-]+", re.IGNORECASE),
    "macos_home_path": re.compile(r"/Users/[A-Za-z0-9._-]+", re.IGNORECASE),
    "private_provider_build_label": re.compile(
        r"\b[A-Z0-9.-]*PROVIDER[0-9]+\b", re.IGNORECASE
    ),
    "openai_key": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{16,}\b"),
    "github_token": re.compile(
        r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"
    ),
    "gitlab_token": re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b"),
    "aws_access_key": re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    "google_api_key": re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    "slack_token": re.compile(r"\b(?:xox[a-z]|xapp)-[A-Za-z0-9-]{10,}\b"),
    "npm_token": re.compile(r"\bnpm_[A-Za-z0-9]{20,}\b"),
    "pypi_token": re.compile(r"\bpypi-[A-Za-z0-9_-]{40,}\b"),
    "stripe_secret": re.compile(r"\b(?:sk|rk)_live_[A-Za-z0-9]{16,}\b"),
    "huggingface_token": re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
    "private_key_header": re.compile(
        r"-{5}BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-{5}"
    ),
    "operational_secret_assignment": re.compile(
        r"(?ix)\b(?:"
        r"api[_ -]?key|api[_ -]?secret|private[_ -]?key|wallet|pool|password|token|"
        r"aws[_ -]?(?:access[_ -]?key[_ -]?id|secret[_ -]?access[_ -]?key|session[_ -]?token)|"
        r"github[_ -]?token|gitlab[_ -]?token|openai[_ -]?api[_ -]?key|"
        r"slack[_ -]?(?:app[_ -]?token|bot[_ -]?token|user[_ -]?token)|"
        r"npm[_ -]?token|pypi[_ -]?token"
        r")\b\s*[:=]\s*(?:"
        r"\"(?:\\.|[^\"\r\n])+\"|"
        r"'(?:\\.|[^'\r\n])+'|"
        r"[^\s,;}\]\r\n]+"
        r")"
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
CREDENTIAL_FIXTURES = {
    "private_provider_build_label": (
        "SYNTHETIC-BUILD-PROVIDER9",
    ),
    "openai_key": ("sk-proj-" + "A" * 24,),
    "github_token": ("ghp_" + "A" * 30, "github_pat_" + "A" * 30),
    "gitlab_token": ("glpat-" + "A" * 24,),
    "aws_access_key": (
        "AKIA" + "ABCDEFGHIJKLMNOP",
        "ASIA" + "QRSTUVWXYZABCDEF",
    ),
    "google_api_key": ("AIza" + "A" * 35,),
    "slack_token": (
        "xoxb-" + "1234567890-ABCDEFGHIJK",
        "xapp-" + "1-ABCDEFGHIJK-1234567890",
        "xoxe-" + "1-ABCDEFGHIJK-1234567890",
    ),
    "npm_token": ("npm_" + "A" * 36,),
    "pypi_token": ("pypi-" + "A" * 48,),
    "stripe_secret": ("sk_live_" + "A" * 24,),
    "huggingface_token": ("hf_" + "A" * 32,),
    "private_key_header": (PRIVATE_KEY_MARKER,),
    "operational_secret_assignment": (
        "AWS_SECRET_ACCESS_KEY=" + "A" * 40,
        "SLACK_APP_TOKEN=" + "A" * 24,
        "password=hunter2",
        "token=secret",
        'password="my pass"',
        "api_key='x'",
    ),
}
PRIVATE_PATH_FIXTURES = {
    "personal_windows_path": (
        BACKSLASH.join(("C:", "Users", "example-user", "private-project")),
    ),
    "unix_home_path": ("/home/example-user/private-project",),
    "macos_home_path": ("/Users/example-user/private-project",),
}


def normalized_text(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


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
        self.assertIn("Fourteen engineering analyses", readme)
        self.assertIn("Twelve named showcase studies", readme)
        self.assertIn("## Scope and safety boundary", readme)
        self.assertIn("## Sanitization method", readme)
        self.assertIn("## Evidence and limitations", readme)
        self.assertIn("synthetic scenarios", readme)
        self.assertIn("do not claim", readme)
        for path in SHOWCASE_PROVENANCE:
            self.assertIn(f"docs/{path.name}", readme)

    def test_media_restart_reconciles_the_published_destination(self) -> None:
        text = normalized_text(
            ROOT / "docs" / "authorized-media-transfer-resilience.md"
        ).lower()
        required = (
            "deterministic destination identity",
            "durable publication receipt",
            "before relaunching another worker",
            "destination and receipt already agree",
            "at most one published result",
            "retry budget exhausted",
            "budget expires with no prior publication",
        )
        for marker in required:
            self.assertIn(marker, text)

    def test_launcher_consolidation_has_one_authority(self) -> None:
        text = normalized_text(
            ROOT / "docs" / "media-tagger-one-active-launcher.md"
        )
        required = (
            "one canonical launcher",
            "one authoritative backend implementation",
            "logic-free forwarder",
            "unsupported-action result",
            "dry-run remains non-mutating",
            "does not promote v0.5.17",
        )
        for marker in required:
            self.assertIn(marker, text)

    def test_botops_control_plane_preserves_authority_boundaries(self) -> None:
        text = normalized_text(
            ROOT / "docs" / "botops-control-plane-cohesion.md"
        )
        required = (
            "v1.23.3 is the user-confirmed Windows control rollback baseline",
            "v1.25.0 is the Windows scan-accepted foundation save state",
            "31-versus-26 registry/dashboard evidence split",
            "without introducing a second Windows process scan",
            "252 source tests",
            "same 252 tests from a fresh exact extraction",
            "57 strict release-verifier checks",
            "22 managed-identity checks",
            "A cached dashboard count cannot overrule",
            "persisted process identifier is never sufficient proof of ownership",
            "full Windows preflight",
            "one disposable low-risk verified child start/stop cycle",
        )
        for marker in required:
            self.assertIn(marker, text)

    def test_current_consolidation_evidence_is_qualified(self) -> None:
        repair = normalized_text(
            ROOT / "docs" / "windows-repair-remediation-governance.md"
        )
        for marker in (
            "v55.33.0 consolidation candidate",
            "91 to 90 retained files",
            "six distinct root BAT actions",
            "no exact duplicate-content groups",
            "retirement of the unproven `00_START_HERE.bat` launcher",
            "v55.29.4 working baseline",
        ):
            self.assertIn(marker, repair)

        crypto = normalized_text(
            ROOT / "docs" / "crypto-spread-bot-reliability.md"
        )
        for marker in (
            "Binance.US Multi-Spread Bot R314",
            "R317 is a later one-capability, one-active-action candidate",
            "one current action registry",
            "no active CLI aliases",
            "remains unpromoted",
        ):
            self.assertIn(marker, crypto)

    def test_gateway_intelligence_core_preserves_local_first_boundary(self) -> None:
        text = normalized_text(
            ROOT / "docs" / "gateway-intelligence-core-evidence.md"
        )
        required = (
            "Gateway Intelligence Core v0.1.4",
            "private package build label is intentionally omitted",
            "91 of 91 source tests",
            "91 of 91 exact-extract tests",
            "23 of 23 deterministic evaluations",
            "54 of 54 managed-identity checks",
            "17 bounded items",
            "Field acceptance remains open for Windows double-click launch",
            "automatic routines remain local",
            "artifact identities remain permanently distinct",
            "acceptance can change disposition and current authority, but never merge, overwrite, or relabel",
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
                raw = path.read_text(encoding="utf-8")
                lower = " ".join(raw.lower().split())
                for heading in required_headings:
                    self.assertIn(heading, raw)
                self.assertTrue(any(marker in lower for marker in provenance_markers))
                self.assertIn("synthetic", lower)
                self.assertRegex(lower, r"\bcannot\b")

    def test_high_value_credential_formats_are_detected(self) -> None:
        for label, values in CREDENTIAL_FIXTURES.items():
            pattern = SENSITIVE_PATTERNS[label]
            for value in values:
                with self.subTest(pattern=label, value_prefix=value[:12]):
                    self.assertIsNotNone(pattern.search(value))

    def test_private_home_path_formats_are_detected(self) -> None:
        for label, values in PRIVATE_PATH_FIXTURES.items():
            pattern = SENSITIVE_PATTERNS[label]
            for value in values:
                with self.subTest(pattern=label, value=value):
                    self.assertIsNotNone(pattern.search(value))

    def test_named_showcases_contain_no_sensitive_or_operational_residue(self) -> None:
        for path in SHOWCASE_PROVENANCE:
            text = path.read_text(encoding="utf-8")
            for label, pattern in SENSITIVE_PATTERNS.items():
                with self.subTest(path=path.relative_to(ROOT), pattern=label):
                    self.assertIsNone(pattern.search(text))


if __name__ == "__main__":
    unittest.main()
