import sqlite3
from datetime import date
from tracker.pricing import calculate_cost

DAILY_WARNING_LIMIT = 0.01   # $0.01
DAILY_HARD_LIMIT    = 0.02   # $0.02

def get_daily_cost() -> float:
    today = date.today().isoformat()
    conn = sqlite3.connect("data/usage.db")
    rows = conn.execute(
        "SELECT model, input_tokens, output_tokens FROM usage WHERE timestamp LIKE ?",
        (f"{today}%",)
    ).fetchall()
    total = 0.0
    for model, input_t, output_t in rows:
        total += calculate_cost(model, input_t, output_t)["total_cost"]
    return round(total, 6)

def check_budget() -> dict:
    current = get_daily_cost()
    status = "ok"
    message = ""

    if current >= DAILY_HARD_LIMIT:
        status = "hard_stop"
        message = f"DAYANDI: Günlük limit aşıldı! ${current:.6f} / ${DAILY_HARD_LIMIT}"
    elif current >= DAILY_WARNING_LIMIT:
        status = "warning"
        message = f"XƏBƏRDARLIQ: Limitə yaxınlaşır! ${current:.6f} / ${DAILY_HARD_LIMIT}"
    else:
        message = f"OK: ${current:.6f} / ${DAILY_HARD_LIMIT}"

    return {
        "status": status,
        "current_cost": current,
        "daily_limit": DAILY_HARD_LIMIT,
        "message": message
    }
