"""Runner with Polymarket connector stub and Discord alerts (dry-run capable).
Replace the POLYM* stubs with real API calls and set DISCORD_WEBHOOK_URL in configs/.env.
"""
import os
import time
import random
import requests
from dotenv import load_dotenv

load_dotenv("../configs/.env")

STARTING_CAPITAL = float(os.getenv("STARTING_CAPITAL", "10"))
MAX_DAILY_LOSS_PCT = float(os.getenv("MAX_DAILY_LOSS_PCT", "5"))
MAX_CONSECUTIVE_LOSSES = int(os.getenv("MAX_CONSECUTIVE_LOSSES", "3"))
POSITION_SIZE_PCT = float(os.getenv("POSITION_SIZE_PCT", "1")) / 100.0
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
POLY_API_KEY = os.getenv("POLY_API_KEY", "")
POLY_API_SECRET = os.getenv("POLY_API_SECRET", "")

DRY_RUN = True

class CircuitBreaker:
    def __init__(self, max_cons_losses, max_daily_loss_pct, starting_capital):
        self.max_cons_losses = max_cons_losses
        self.max_daily_loss = starting_capital * (max_daily_loss_pct / 100.0)
        self.loss_streak = 0
        self.daily_loss = 0.0

    def record_result(self, pnl):
        if pnl < 0:
            self.loss_streak += 1
            self.daily_loss += -pnl
        else:
            self.loss_streak = 0

    def tripped(self):
        return self.loss_streak >= self.max_cons_losses or self.daily_loss >= self.max_daily_loss


def send_discord_alert(message):
    if not DISCORD_WEBHOOK_URL:
        return
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message}, timeout=5)
    except Exception as e:
        print("Failed to send Discord alert:", e)


def fetch_markets_stub():
    """Polymarket connector stub — replace with real API calls.
    Return a list of market dicts the strategy will evaluate.
    """
    # Example stubbed markets
    return [{"id": "m1", "name": "Example Market 1"}, {"id": "m2", "name": "Example Market 2"}]


def example_strategy(market):
    # placeholder strategy: random win/loss equivalent to realised PnL
    pnl = random.uniform(-1.0, 3.0)
    return pnl


def main():
    cb = CircuitBreaker(MAX_CONSECUTIVE_LOSSES, MAX_DAILY_LOSS_PCT, STARTING_CAPITAL)
    capital = STARTING_CAPITAL
    total_trades = 0

    send_discord_alert(f"Starting run: starting capital={capital}")

    markets = fetch_markets_stub()
    for market in markets:
        if cb.tripped():
            send_discord_alert("Circuit breaker tripped — stopping trading loop.")
            print("Circuit breaker tripped — stopping trading loop.")
            break

        # In live mode here we'd compute signals and place orders; scaffold runs example_strategy
        pnl = example_strategy(market)
        cb.record_result(pnl)
        capital += pnl
        total_trades += 1
        print(f"Trade {total_trades} on {market['id']}: PnL={pnl:.2f}, capital={capital:.2f}, loss_streak={cb.loss_streak}")

        # Send a summary per trade in dry-run mode only if webhook is set
        if DISCORD_WEBHOOK_URL:
            send_discord_alert(f"Trade {total_trades} on {market['id']}: PnL={pnl:.2f}, capital={capital:.2f}")

        time.sleep(0.5)

    send_discord_alert(f"Run complete. Final capital={capital:.2f}, trades={total_trades}")
    print("Run complete. Final capital:", capital)

if __name__ == '__main__':
    main()
