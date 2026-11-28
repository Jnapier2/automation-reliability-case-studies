# Configuration Change Preview

Preview a change to a fictional application's settings. This Windows demo shows how an operator can see the current and proposed value, how a protected setting is handled, and what happens when the reviewed file changes.

Requires Python 3.11 or newer on Windows. In the extracted folder, run:

```powershell
python -I -B .\review.py
python -I -B .\review.py --field execution_mode --value 3
```

The first command previews changing the bundled sample from two parallel jobs to three. The second is rejected because execution mode is protected. If you change the bundled sample and try again, the demo asks for a fresh copy. The preview leaves the sample unchanged.

This is an offline technical-evaluation demo using fictional settings. It previews only its bundled file. It cannot edit application configuration or activate a setting. The rights notice for the download is included as `LICENSE.md`.
