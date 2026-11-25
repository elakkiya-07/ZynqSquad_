"""Recompute Table IV of the DPR (discard share per rule and threshold) from results/tiles.csv."""
import sys
import pandas as pd

csv = sys.argv[1] if len(sys.argv) > 1 else "results/tiles.csv"
df = pd.read_csv(csv)
N = 256 * 256
cloud = df.cloud_cnt / N
joint = (df.cloud_cnt + df.water_cnt) / N

print(f"Tiles: {len(df)}")
print(f"{'Threshold':>10} {'Cloud-only':>12} {'Cloud+water':>12}")
for th in (0.60, 0.70, 0.80):
    print(f"{th:>10.0%} {100 * (cloud >= th).mean():>11.1f}% {100 * (joint >= th).mean():>11.1f}%")
print(f"Tiles with cloud+water between 65% and 75%: {((joint >= 0.65) & (joint < 0.75)).sum()}")
