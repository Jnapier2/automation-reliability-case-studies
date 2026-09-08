# Automation Reliability Case Studies

[![CI](https://github.com/Jnapier2/automation-reliability-case-studies/actions/workflows/ci.yml/badge.svg)](https://github.com/Jnapier2/automation-reliability-case-studies/actions/workflows/ci.yml)

Fifteen short design analyses examine how incomplete evidence, interrupted work, and inconsistent system state affect reliability. The deliverables are the documents linked below. They are not fifteen released software products.

## Studies

- [Ambiguous transaction outcomes](docs/exchange-automation-reconciliation.md)
- [Compute-worker health](docs/compute-worker-supervision.md)
- [Interrupted media transfers](docs/authorized-media-transfer-resilience.md)
- [Reviewable media organization](docs/media-tagger-one-active-launcher.md)
- [Consistent operations views](docs/botops-control-plane-cohesion.md)
- [Compute readiness and progress](docs/gpu-mining-readiness.md)
- [Cross-system data consistency](docs/crypto-spread-bot-reliability.md)
- [Decision-input quality](docs/prediction-market-data-quality.md)
- [Version-specific evidence](docs/prediction-market-save-state-reconciliation.md)
- [Changing external interfaces](docs/prediction-market-structural-parity.md)
- [Diagnostic confidence](docs/local-network-guard-evidence.md)
- [Evidence and interpretation](docs/gateway-intelligence-core-evidence.md)
- [Evaluating remediation outcomes](docs/windows-repair-remediation-governance.md)
- [Cross-platform readiness](docs/sagemath-wsl-manager-recovery.md)
- [Deliverable completeness](docs/release-acceptance-fail-closed.md)

## Evidence and limitations

These studies discuss synthetic scenarios and general review concerns. They do not claim measured production outcomes or demonstrate executable integrations. Documentation checks validate file format, links, metadata, and privacy rules; they do not prove runtime behavior.

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
