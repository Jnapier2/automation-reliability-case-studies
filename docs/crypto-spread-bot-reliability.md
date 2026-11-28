# Cross-system data consistency

**Deliverable:** Design-analysis document. **Companion:** Offline Windows demo. **Evidence type:** Source review and synthetic runtime checks.

## Problem

A repeated record may be an exact replay or a disagreement about an observation already accepted. Treating both as duplicates can hide a discrepancy from the people reviewing the evidence.

## Practical value

The reviewed implementations distinguish an exact replay from conflicting evidence. The existing observation stays available while the conflict is flagged for review, giving the operator a clear reason to investigate.

## Try the example

Download **Evidence Reconciliation** from the [Windows demos release](https://github.com/Jnapier2/automation-reliability-case-studies/releases/tag/windows-demos-2026-11-28). Follow the [demo instructions](../demos/evidence-reconciliation/README.md) and compare the output with the bundled fictional records.

## Evidence and limitations

Source comparison across two related editions confirmed that the released correction rechecks stored evidence when deciding whether to flag a conflict. The public demo is a separate, in-memory implementation covering exact replays, conflicting observations, and two observations arriving together. Its checks use fictional records. Persistent accounting, live services, and financial results are outside this demo.

[All studies](../README.md)

Copyright © 2026 Gateway Information Group LLC. All rights reserved.
