# Evidence Reconciliation

Review a batch of fictional records containing both an exact replay and conflicting evidence. The demo shows what was accepted, what was ignored as a duplicate, and what needs a person's review. A conflicting report leaves the previously accepted observation intact and visible.

Requires Python 3.11 or newer on Windows. In the extracted folder, run:

```powershell
python -I -B .\review.py
```

Read the JSON in the terminal alongside `sample-events.json`. The first report for sample A is accepted. Its exact replay is labeled duplicate. The differing report is labeled review required. Sample B is accepted independently.

This is an offline technical-evaluation demo using fictional records. The output is an evidence review, with no balance, financial result, account access, or order execution. State lasts for the run. The rights notice for the download is included as `LICENSE.md`.
