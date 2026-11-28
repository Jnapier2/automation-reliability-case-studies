"""Review the included fictional evidence in memory."""
import json
from pathlib import Path
from threading import Lock

SAMPLE = Path(__file__).resolve().parent / "sample-events.json"
MAX_SAMPLE_BYTES = 4096


class EvidenceReview:
    def __init__(self):
        self._accepted = {}
        self._needs_review = set()
        self._lock = Lock()

    def observe(self, event_id, units):
        with self._lock:
            if event_id not in self._accepted:
                self._accepted[event_id] = units
                return "accepted"
            if self._accepted[event_id] == units:
                return "duplicate"
            self._needs_review.add(event_id)
            return "review_required"

    def snapshot(self):
        with self._lock:
            return {
                "accepted_observations": dict(self._accepted),
                "needs_review": sorted(self._needs_review),
            }


def load_sample():
    with SAMPLE.open("rb") as source:
        data = source.read(MAX_SAMPLE_BYTES + 1)
    if len(data) > MAX_SAMPLE_BYTES:
        raise ValueError("Sample exceeds the size limit.")
    rows = json.loads(data)
    if not isinstance(rows, list) or not 1 <= len(rows) <= 20:
        raise ValueError("Expected a bounded list of fictional observations.")
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"event_id", "reported_units"}:
            raise ValueError("Unexpected observation fields.")
        event_id = row["event_id"]
        units = row["reported_units"]
        if (
            not isinstance(event_id, str)
            or event_id not in {"sample-A", "sample-B"}
            or type(units) is not int
            or not 0 <= units <= 100_000
        ):
            raise ValueError("Invalid fictional observation.")
    return rows


def main():
    try:
        rows = load_sample()
    except (OSError, ValueError):
        print(json.dumps({"error": "Use a valid copy of the bundled fictional sample."}))
        return 2
    review = EvidenceReview()
    decisions = []
    for row in rows:
        decision = review.observe(row["event_id"], row["reported_units"])
        decisions.append({**row, "decision": decision})
    print(json.dumps({
        "sample": "synthetic",
        "decisions": decisions,
        **review.snapshot(),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
