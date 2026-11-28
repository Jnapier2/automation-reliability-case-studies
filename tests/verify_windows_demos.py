"""Build deterministic public archives and verify their extracted Windows entry points."""
import argparse
import hashlib
import importlib.util
import json
import os
import stat
import subprocess
import sys
import tempfile
import threading
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMOS = {
    "configuration-change-preview": "sample-preferences.json",
    "evidence-reconciliation": "sample-events.json",
}


def build_demo(name, sample, output):
    asset = output / f"{name}-windows.zip"
    source = ROOT / "demos" / name
    members = {
        "LICENSE.md": ROOT / "LICENSE.md",
        "README.md": source / "README.md",
        "review.py": source / "review.py",
        sample: source / sample,
    }
    with zipfile.ZipFile(asset, "x") as archive:
        for relative, path in members.items():
            data = path.read_bytes().replace(b"\r\n", b"\n")
            entry = zipfile.ZipInfo(f"{name}/{relative}", (2026, 11, 28, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(entry, data, compress_type=zipfile.ZIP_STORED)
    digest = hashlib.sha256(asset.read_bytes()).hexdigest()
    with asset.with_suffix(".zip.sha256").open("x", encoding="ascii", newline="\n") as sidecar:
        sidecar.write(f"{digest}  {asset.name}\n")
    return asset, digest, tuple(members)


def call_demo(extracted, cwd, args=(), status=0):
    result = subprocess.run(
        [sys.executable, "-I", "-B", str(extracted / "review.py"), *args],
        cwd=cwd, capture_output=True, text=True, encoding="utf-8", timeout=15, check=False,
    )
    if result.returncode != status or result.stderr:
        raise RuntimeError(f"Unexpected demo exit: {result.returncode}, expected {status}.")
    return json.loads(result.stdout)


def test_configuration(extracted, caller):
    fixture = extracted / DEMOS["configuration-change-preview"]
    exact = fixture.read_bytes()
    assert call_demo(extracted, caller) == {
        "status": "preview_ready", "field": "max_parallel_jobs",
        "current": 2, "proposed": 3, "applied": False,
    }
    assert call_demo(extracted, caller, ("--value", "4"))["proposed"] == 4
    assert call_demo(extracted, caller, ("--field", "execution_mode"), 2) == {
        "status": "protected_or_unknown",
    }
    assert call_demo(extracted, caller, ("--value", "5"), 2)["status"] == "invalid_value"
    assert fixture.read_bytes() == exact
    modified = exact.replace(b'"max_parallel_jobs": 2', b'"max_parallel_jobs": 1')
    assert modified != exact
    fixture.write_bytes(modified)
    assert call_demo(extracted, caller, status=2)["status"] == "review_required"
    assert fixture.read_bytes() == modified
    fixture.unlink()
    assert call_demo(extracted, caller, status=2)["status"] == "sample_unavailable"
    fixture.write_bytes(exact)
    print("PASS configuration: default, boundary, protected, stale, missing, no-write", flush=True)


def test_evidence(extracted, caller):
    fixture = extracted / DEMOS["evidence-reconciliation"]
    exact = fixture.read_bytes()
    actual = call_demo(extracted, caller)
    assert actual["sample"] == "synthetic"
    assert [r["decision"] for r in actual["decisions"]] == [
        "accepted", "duplicate", "review_required", "accepted",
    ]
    assert actual["accepted_observations"] == {"sample-A": 12, "sample-B": 4}
    assert actual["needs_review"] == ["sample-A"] and fixture.read_bytes() == exact

    # Exercise competing observations using the exact code from the extracted ZIP.
    spec = importlib.util.spec_from_file_location("packaged_review", extracted / "review.py")
    review_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(review_module)
    for inputs, expected in [
        ((12, 12), ["accepted", "duplicate"]),
        ((12, 15), ["accepted", "review_required"]),
    ]:
        review = review_module.EvidenceReview()
        start = threading.Barrier(2)

        def observe(units):
            start.wait(timeout=5)
            return review.observe("sample-A", units)

        with ThreadPoolExecutor(2) as pool:
            observed = list(pool.map(observe, inputs))
        assert sorted(observed) == expected
        first = inputs[observed.index("accepted")]
        holds = ["sample-A"] if inputs[0] != inputs[1] else []
        assert review.snapshot() == {
            "accepted_observations": {"sample-A": first}, "needs_review": holds,
        }
    fixture.write_bytes(b'[{"event_id":"sample-A","reported_units":true}]')
    assert "error" in call_demo(extracted, caller, status=2)
    fixture.write_bytes(exact)
    print("PASS evidence: replay, conflict, distinct records, competing inputs, invalid sample", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    opts = parser.parse_args()
    if os.name != "nt":
        parser.error("Run this exact-archive verification on Windows.")
    if not sys.dont_write_bytecode or not __debug__:
        parser.error("Run the verifier with python -B and assertions enabled.")
    output = opts.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    for name, sample in DEMOS.items():
        asset, digest, entries = build_demo(name, sample, output)
        with tempfile.TemporaryDirectory(prefix="Windows demo check ", dir=output) as workspace:
            scratch = Path(workspace)
            extracted = scratch / name
            extracted.mkdir()
            caller = scratch / "Unrelated caller"
            caller.mkdir()
            with zipfile.ZipFile(asset) as archive:
                assert archive.namelist() == [f"{name}/{entry}" for entry in entries]
                assert archive.testzip() is None
                for entry in entries:
                    (extracted / entry).write_bytes(archive.read(f"{name}/{entry}"))
            check = test_configuration if name == "configuration-change-preview" else test_evidence
            check(extracted, caller)
            assert not list(caller.iterdir())
            assert set(e.name for e in extracted.iterdir()) == set(entries)
        assert hashlib.sha256(asset.read_bytes()).hexdigest() == digest
        print(f"VERIFIED_ARCHIVE_SHA256={digest} {asset.name}", flush=True)


if __name__ == "__main__":
    main()
