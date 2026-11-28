"""Preview an allowed change to the included fictional configuration."""
import argparse
import hashlib
import json
from pathlib import Path

SAMPLE = Path(__file__).resolve().parent / "sample-preferences.json"
SAMPLE_SHA256 = "cb6899991fd68a906262308f5b9ad07d00926cdc4dc45a3c7f46c9a457eb6a24"
MAX_SAMPLE_BYTES = 4096
EDITABLE_FIELD = "max_parallel_jobs"


def preview(field, proposed):
    if field != EDITABLE_FIELD:
        return {"status": "protected_or_unknown"}, 2
    if not 1 <= proposed <= 4:
        return {"status": "invalid_value", "minimum": 1, "maximum": 4}, 2
    try:
        with SAMPLE.open("rb") as source:
            data = source.read(MAX_SAMPLE_BYTES + 1)
    except OSError:
        return {"status": "sample_unavailable"}, 2
    if len(data) > MAX_SAMPLE_BYTES or hashlib.sha256(data).hexdigest() != SAMPLE_SHA256:
        return {"status": "review_required", "reason": "Bundled sample changed."}, 2
    settings = json.loads(data)
    return {
        "status": "preview_ready",
        "field": field,
        "current": settings[field],
        "proposed": proposed,
        "applied": False,
    }, 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field", default=EDITABLE_FIELD)
    parser.add_argument("--value", type=int, default=3)
    options = parser.parse_args()
    result, status = preview(options.field, options.value)
    print(json.dumps(result, indent=2))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
