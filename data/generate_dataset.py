import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json

np.random.seed(42)
random.seed(42)

N = 10000
GENRES = ["Action", "Comedy", "Drama", "Thriller", "Horror", "Romance",
          "Sci-Fi", "Documentary", "Animation", "Crime"]

# ── Subscriber profiles ──────────────────────────────────────────────────────
subscriber_ids = [f"SUB_{str(i).zfill(5)}" for i in range(1, N + 1)]

tiers = np.random.choice(["Basic", "Standard", "Premium"],
                         size=N, p=[0.35, 0.45, 0.20])

age_groups = np.random.choice(["18-24", "25-34", "35-44", "45+"],
                               size=N, p=[0.20, 0.35, 0.25, 0.20])

regions = np.random.choice(["Northeast", "South", "Midwest", "West"],
                            size=N, p=[0.22, 0.38, 0.22, 0.18])

# Signup dates spread across last 24 months
base_date = datetime(2023, 1, 1)
signup_days = np.random.randint(0, 730, size=N)
signup_dates = [base_date + timedelta(days=int(d)) for d in signup_days]
months_subscribed = [max(1, (datetime(2024, 12, 31) - s).days // 30) for s in signup_dates]

num_profiles = np.random.choice([1, 2, 3, 4, 5], size=N, p=[0.30, 0.30, 0.20, 0.15, 0.05])

# ── Behavioral features ──────────────────────────────────────────────────────
# Days to first watch — higher = more at risk
days_to_first_watch = np.random.exponential(scale=3, size=N).astype(int)
days_to_first_watch = np.clip(days_to_first_watch, 0, 30)

# Avg weekly watch hours — tier influences this
tier_hours = {"Basic": (2, 1.5), "Standard": (5, 2.5), "Premium": (10, 4)}
avg_weekly_watch_hours = np.array([
    max(0, np.random.normal(tier_hours[t][0], tier_hours[t][1]))
    for t in tiers
])
avg_weekly_watch_hours = np.round(avg_weekly_watch_hours, 1)

# Genre diversity score 0-1
genre_diversity_score = np.round(np.random.beta(a=2, b=2, size=N), 2)

# Pct content completed
pct_content_completed = np.round(np.random.beta(a=5, b=2, size=N), 2)

# Days since last watch
days_since_last_watch = np.random.exponential(scale=8, size=N).astype(int)
days_since_last_watch = np.clip(days_since_last_watch, 0, 90)

# Favorite genre (most watched)
favorite_genres = np.random.choice(GENRES, size=N)

# Number of titles watched
num_titles_watched = np.random.poisson(lam=15, size=N)
num_titles_watched = np.clip(num_titles_watched, 0, 80)

# ── Churn logic ──────────────────────────────────────────────────────────────
# Base churn probability per tier
tier_base = {"Basic": 0.15, "Standard": 0.07, "Premium": 0.04}
churn_prob = np.array([tier_base[t] for t in tiers])

# Risk factors that increase churn probability
# 1. Slow to first watch
churn_prob += np.where(days_to_first_watch > 7, 0.25, 0)

# 2. Low engagement
churn_prob += np.where(avg_weekly_watch_hours < 2, 0.20, 0)
churn_prob += np.where(avg_weekly_watch_hours < 1, 0.10, 0)  # extra penalty

# 3. Inactive recently
churn_prob += np.where(days_since_last_watch > 14, 0.18, 0)
churn_prob += np.where(days_since_last_watch > 30, 0.12, 0)  # extra penalty

# 4. Low genre diversity (stuck/bored)
churn_prob += np.where(genre_diversity_score < 0.25, 0.10, 0)

# 5. New subscriber risk window
churn_prob += np.where(np.array(months_subscribed) < 3, 0.08, 0)

# 6. Low completion rate
churn_prob += np.where(pct_content_completed < 0.4, 0.07, 0)

# Protective factors
churn_prob -= np.where(num_profiles >= 3, 0.05, 0)
churn_prob -= np.where(np.array(months_subscribed) > 12, 0.06, 0)
churn_prob -= np.where(avg_weekly_watch_hours > 8, 0.08, 0)

churn_prob = np.clip(churn_prob, 0.01, 0.95)
churned = np.random.binomial(1, churn_prob, size=N)

# Churn date (within their subscription window)
churn_dates = []
for i in range(N):
    if churned[i] == 1:
        max_days = max(1, months_subscribed[i] * 30)
        churn_day = random.randint(1, max_days)
        churn_dates.append(signup_dates[i] + timedelta(days=churn_day))
    else:
        churn_dates.append(None)

# ── Assemble DataFrame ────────────────────────────────────────────────────────
df = pd.DataFrame({
    "subscriber_id": subscriber_ids,
    "signup_date": [d.strftime("%Y-%m-%d") for d in signup_dates],
    "subscription_tier": tiers,
    "age_group": age_groups,
    "region": regions,
    "num_profiles": num_profiles,
    "months_subscribed": months_subscribed,
    "days_to_first_watch": days_to_first_watch,
    "avg_weekly_watch_hours": avg_weekly_watch_hours,
    "days_since_last_watch": days_since_last_watch,
    "genre_diversity_score": genre_diversity_score,
    "pct_content_completed": pct_content_completed,
    "num_titles_watched": num_titles_watched,
    "favorite_genre": favorite_genres,
    "churned": churned,
    "churn_date": [d.strftime("%Y-%m-%d") if d else None for d in churn_dates],
})

# ── Save outputs ──────────────────────────────────────────────────────────────
df.to_csv("/mnt/user-data/outputs/streaming_subscribers.csv", index=False)

# Quick validation summary
print("=== Dataset Summary ===")
print(f"Total subscribers: {len(df):,}")
print(f"Churned: {df['churned'].sum():,} ({df['churned'].mean()*100:.1f}%)")
print(f"\nChurn by tier:")
print(df.groupby("subscription_tier")["churned"].agg(["sum", "mean"]).rename(columns={"sum": "churned_count", "mean": "churn_rate"}).round(3).to_string())
print(f"\nChurn by days_to_first_watch > 7:")
print(df.groupby(df["days_to_first_watch"] > 7)["churned"].mean().round(3).to_string())
print(f"\nChurn by avg_weekly_watch_hours < 2:")
print(df.groupby(df["avg_weekly_watch_hours"] < 2)["churned"].mean().round(3).to_string())
print(f"\nChurn by months_subscribed < 3:")
print(df.groupby(df["months_subscribed"] < 3)["churned"].mean().round(3).to_string())
print(f"\nColumns: {list(df.columns)}")
print(f"\nFirst 3 rows:")
print(df.head(3).to_string())
