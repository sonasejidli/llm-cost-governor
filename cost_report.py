import sqlite3
from tracker.pricing import calculate_cost

conn = sqlite3.connect("data/usage.db")
rows = conn.execute(
    "SELECT timestamp, model, input_tokens, output_tokens FROM usage ORDER BY timestamp"
).fetchall()

print(f"{'Tarix':<25} {'Model':<20} {'Input':>8} {'Output':>8} {'Xərc ($)':>10}")
print("-" * 75)

grand_total = 0.0
for row in rows:
    timestamp, model, input_t, output_t = row
    cost = calculate_cost(model, input_t, output_t)
    grand_total += cost["total_cost"]
    print(f"{timestamp:<25} {model:<20} {input_t:>8} {output_t:>8} {cost['total_cost']:>10.6f}")

print("-" * 75)
print(f"{'Ümumi xərc':>63} ${grand_total:.6f}")
