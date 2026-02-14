Runbook & Safety Checklist

1) Fill env: cp configs/.env.template .env and paste secrets.
2) Install deps: pip install -r runner/requirements.txt
3) Dry run: python runner/main.py (uses example strategy)
4) For live runs: replace example_strategy with API-backed logic and add authentication.
5) Monitor: use Discord webhook for alerts and daily summaries.

Critical safety defaults (change only with caution):
- MAX_CONSECUTIVE_LOSSES=3
- MAX_DAILY_LOSS_PCT=5
- Keep allocations tiny while testing

If you want a patch/PR: run `git checkout -b chore/openclaw-trading-setup && git add trading && git commit -m "chore: add OpenClaw trading scaffold" && git format-patch -1 HEAD --stdout > /tmp/openclaw_trading_scaffold.patch` and send me the patch file or paste it back here.
