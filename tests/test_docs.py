from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
BACKSLASH = chr(92)
PRIVATE_KEY_MARKER = "-" * 5 + "BEGIN PRIVATE KEY" + "-" * 5
SHOWCASE_PROVENANCE = {path: () for path in (ROOT / "docs").glob("*.md")}
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
    "private_provider_build_label": ("SYNTHETIC-BUILD-PROVIDER9",),
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
        self.assertGreaterEqual(len(files), 18)
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

    def test_document_inventory_and_scope(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertEqual(len(SHOWCASE_PROVENANCE), 15)
        for path in SHOWCASE_PROVENANCE:
            with self.subTest(path=path.name):
                self.assertIn(f"docs/{path.name}", readme)
                body = path.read_text(encoding="utf-8")
                self.assertIn("**Deliverable:** Design-analysis document.", body)
                self.assertIn("## Evidence and limitations", body)

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
        for path in self.markdown_files():
            text = path.read_text(encoding="utf-8")
            for label, pattern in SENSITIVE_PATTERNS.items():
                with self.subTest(path=path.relative_to(ROOT), pattern=label):
                    self.assertIsNone(pattern.search(text))


if __name__ == "__main__":
    unittest.main()
