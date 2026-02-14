OpenClaw trading scaffold

What's here:
- agent/ : OpenClaw agent prompt and helper
- runner/: Python runner that connects to Polymarket (example) and executes strategies
- configs/.env.template : environment variable names (do NOT add secrets here)
- docs/ : runbook and safety checklist

How to use (local patch flow):
1) Copy configs/.env.template -> .env and fill secrets
2) Install dependencies: pip install -r runner/requirements.txt
3) Run locally for dry-run: python runner/main.py --dry-run

Safety: default circuit-breaker enabled: max_consecutive_losses=3, max_daily_loss_pct=5
