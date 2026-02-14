"""Simple runner example (dry-run capable).
This is a minimal scaffold — replace Polymarket API calls with real endpoints.
"""
import os
import time
import random
from dotenv import load_dotenv

load_dotenv("../configs/.env")

STARTING_CAPITAL = float(os.getenv("STARTING_CAPITAL", "10"))
MAX_DAILY_LOSS_PCT = float(os.getenv("MAX_DAILY_LOSS_PCT", "5"))
MAX_CONSECUTIVE_LOSSES = int(os.getenv("MAX_CONSECUTIVE_LOSSES", "3"))
POSITION_SIZE_PCT = float(os.getenv("POSITION_SIZE_PCT", "1")) / 100.0

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


def example_strategy(market):
    # placeholder strategy: random win/loss
    pnl = random.uniform(-1.0, 3.0)
    return pnl


def main():
    cb = CircuitBreaker(MAX_CONSECUTIVE_LOSSES, MAX_DAILY_LOSS_PCT, STARTING_CAPITAL)
    capital = STARTING_CAPITAL
    trades = 0

    while trades < 10:  # small loop for scaffold
        market = {}  # replace with API call
        pnl = example_strategy(market)
        cb.record_result(pnl)
        capital += pnl
        trades += 1
        print(f"Trade {trades}: PnL={pnl:.2f}, capital={capital:.2f}, loss_streak={cb.loss_streak}")
        if cb.tripped():
            print("Circuit breaker tripped — stopping trading loop.")
            break
        time.sleep(0.5)

    print("Run complete. Final capital:", capital)

if __name__ == '__main__':
    main()
