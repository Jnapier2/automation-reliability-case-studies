# Automation Reliability Case Studies

[![CI](https://github.com/Jnapier2/automation-reliability-case-studies/actions/workflows/ci.yml/badge.svg)](https://github.com/Jnapier2/automation-reliability-case-studies/actions/workflows/ci.yml)

These design analyses examine how incomplete evidence, interrupted work, and inconsistent system state affect reliability. Each document gives reviewers a way to examine an operating decision and trace it back to the available evidence.

## Start with the evidence

- **Inspect a captured result:** [Diagnostic archive accountability](docs/diagnostic-archive-accountability.md) pairs a concrete bookkeeping defect with a [generated synthetic fixture result](examples/archive-inventory.json) and a [captured Windows export review](examples/windows-export-review.json). Compare what was recognized and preserved, and how partial capture was reported.
- **Review a user-facing report:** [Interrupted media transfers](docs/authorized-media-transfer-resilience.md) explains the included [text report](examples/collection-report.txt) and [HTML report](examples/collection-report.html). Download and open the HTML file locally to see its rendered layout; GitHub's file viewer displays the source.
- **Explore an operations decision:** [Consistent operations views](docs/botops-control-plane-cohesion.md) shows why missing observations, muted incidents, and healthy operation need different interpretations. Its scenarios are illustrative rather than captured runtime output.

Each study identifies the problem, practical usefulness, evidence method, and limitations. The examples support those stated boundaries; they do not operate the private applications.

## Try the offline Windows demos

- **Configuration Change Preview** shows an allowed settings change and how a protected or changed file is handled. [Review the case and demo instructions](docs/configuration-change-preview.md).
- **Evidence Reconciliation** shows how an exact replay and conflicting evidence lead to different decisions. [Review the case and demo instructions](docs/crypto-spread-bot-reliability.md).

The [Windows demo release](https://github.com/Jnapier2/automation-reliability-case-studies/releases/tag/windows-demos-2026-11-28) includes both ZIPs and their checksums. Each demo runs on fictional input using Python 3.11 or newer.

## Studies

- [Ambiguous transaction outcomes](docs/exchange-automation-reconciliation.md)
- [Compute-worker health](docs/compute-worker-supervision.md)
- [Interrupted media transfers](docs/authorized-media-transfer-resilience.md)
- [Reviewable media organization](docs/media-tagger-one-active-launcher.md)
- [Consistent operations views](docs/botops-control-plane-cohesion.md)
- [Compute readiness and progress](docs/gpu-mining-readiness.md)
- [Cross-system data consistency](docs/crypto-spread-bot-reliability.md)
- [Reviewing configuration changes](docs/configuration-change-preview.md)
- [Decision-input quality](docs/prediction-market-data-quality.md)
- [Version-specific evidence](docs/prediction-market-save-state-reconciliation.md)
- [Changing external interfaces](docs/prediction-market-structural-parity.md)
- [Diagnostic confidence](docs/local-network-guard-evidence.md)
- [Investigating an incomplete Windows wake](docs/windows-wake-incident-evidence.md)
- [Diagnostic archive accountability](docs/diagnostic-archive-accountability.md)
- [Evidence and interpretation](docs/gateway-intelligence-core-evidence.md)
- [Evaluating remediation outcomes](docs/windows-repair-remediation-governance.md)
- [Cross-platform readiness](docs/sagemath-wsl-manager-recovery.md)
- [Deliverable completeness](docs/release-acceptance-fail-closed.md)

## Evidence and limitations

These studies discuss synthetic scenarios and general review concerns. [Consistent operations views](docs/botops-control-plane-cohesion.md) and [Diagnostic confidence](docs/local-network-guard-evidence.md) include source-reviewed distinctions with manually written illustrative scenarios. [Interrupted media transfers](docs/authorized-media-transfer-resilience.md) includes a generated report from an inspected private candidate, with its fixture method and limits. [Diagnostic archive accountability](docs/diagnostic-archive-accountability.md) includes source-fixture and Windows diagnostic-export observations, with a failing earlier recognition revision and a passing corrected revision. The studies describe specific observations and fictional examples. The two Windows demos come with separate runtime checks for their packaged entry points. Their results cover the bundled examples.

## Related runnable work

- [BotOps Manager](https://github.com/Jnapier2/botops-manager)
- [MediaTaggerBot](https://github.com/Jnapier2/media-tagger-bot)
- [Digital Asset Governance Audit](https://github.com/Jnapier2/digital-asset-governance-case-study)

Each linked repository describes its own source, examples, tests, and limitations.

## Documentation checks

```bash
python -m unittest discover -s tests -v
```

See [LICENSE.md](LICENSE.md) and [SECURITY.md](SECURITY.md).

[Portfolio](https://jerry-napier-portfolio.netlify.app/) · [GitHub profile](https://github.com/Jnapier2)

Copyright © 2026 Gateway Information Group LLC. All rights reserved.
