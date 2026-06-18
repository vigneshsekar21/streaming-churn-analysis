# Streaming Subscriber Churn Analysis

Every streaming service's core business problem is the same: subscribers cancel, and most companies don't know why until it's too late. This project simulates that problem from the ground up — building a realistic subscriber dataset, identifying the behavioral patterns that predict churn, and translating findings into actionable recommendations a product or growth team could act on immediately.

---

## Business objective

Identify which subscriber behaviors and content gaps predict cancellation, and recommend data-driven retention interventions for a fictional streaming service.

**Core questions:**
- Which behavioral patterns (inactivity windows, low genre diversity, slow onboarding) most strongly predict churn?
- Are there content gaps — missing genres, thin catalog depth — that correlate with subscriber drop-off?
- Which segments are highest risk, and what does a targeted retention strategy look like for each?

---

## Key findings

> *(To be updated after modeling in Week 3)*

Preliminary findings from exploratory analysis:

- Subscribers who don't watch within **7 days of signup** churn at **2.3x the rate** of those who do — suggesting onboarding is the single highest-leverage intervention point
- **Basic tier** subscribers churn at 30% vs 5.7% for Premium — but tier alone is a proxy; low engagement hours is the underlying driver
- Subscribers averaging **under 2 hours/week** churn at 40% vs 10% for engaged users
- New subscribers **(under 3 months)** are the highest-risk cohort at 25% churn

---

## Project structure

```
streaming-churn-analysis/
├── README.md
├── data/
│   └── generate_dataset.py       # Synthetic dataset generation with realistic churn logic
├── notebooks/
│   ├── 01_eda.ipynb              # Exploratory analysis, cohort retention, KPI deep-dives
│   └── 02_modeling.ipynb         # Churn model, segmentation, feature importance
├── dashboard/
│   └── tableau_notes.md          # Link to Tableau Public dashboard + design decisions
└── memo/
    └── business_memo.pdf         # 1-page executive summary with recommendations
```

---

## Dataset

The dataset is fully synthetic — generated in Python using realistic distributions and industry-benchmarked churn rates (~17% overall, ranging from 6% for Premium to 30% for Basic tier subscribers).

**10,000 subscribers across 16 features:**

| Feature | Description |
|---|---|
| `subscription_tier` | Basic / Standard / Premium |
| `days_to_first_watch` | Days between signup and first content watched |
| `avg_weekly_watch_hours` | Average weekly engagement |
| `days_since_last_watch` | Recency of last session |
| `genre_diversity_score` | 0–1 score of genre breadth watched |
| `pct_content_completed` | Share of titles watched to completion |
| `months_subscribed` | Tenure at time of observation |
| `churned` | Binary churn label (target variable) |

Content metadata (genres, ratings, popularity) is enriched from the **TMDB public API**.

To generate the dataset locally:
```bash
pip install pandas numpy
python data/generate_dataset.py
```

---

## Tech stack

| Layer | Tools |
|---|---|
| Data generation | Python, NumPy, pandas |
| Analysis & SQL | DuckDB, pandas |
| Modeling | scikit-learn (logistic regression, decision tree) |
| Visualization | Tableau Public |
| Content metadata | TMDB API |

---

## Dashboard

*(Tableau Public link — coming Week 4)*

The dashboard covers four views:
- Churn rate by segment and tier
- Cohort retention curves by signup month
- Behavioral feature distributions (churned vs retained)
- Content gap analysis by genre

---

## Business memo

The full 1-page memo with findings and recommendations is in `/memo/business_memo.pdf`.

**Three recommendations (preview):**
1. Launch a **Day 1–7 onboarding nudge** campaign targeting users who haven't watched yet — email or push notification with a personalized content recommendation
2. Introduce a **Basic tier engagement threshold alert** — flag accounts under 2 hrs/week for a proactive retention offer before they cancel
3. Audit **content depth in high-churn genres** — if subscribers who favor a specific genre churn more, it may indicate a catalog gap worth addressing with licensing or original content

---

## About

Built by **Vignesh Sekar** as a portfolio project targeting Business/Product Analytics roles in the streaming and entertainment space.

M.S. Computational Data Analytics — Georgia Institute of Technology  
[LinkedIn](https://linkedin.com/in/vignesh-sekar-/) · [Email](mailto:vigneshsekar21@gmail.com)
