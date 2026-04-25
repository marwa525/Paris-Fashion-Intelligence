# 🗼 Paris Fashion Intelligence

Live NLP sentiment dashboard for luxury fashion brands.

## Overview

The fashion industry generates millions of data points daily — runway coverage, product launches, executive moves, controversies. Most of this signal is unstructured text scattered across news outlets, blogs, and social platforms.

Paris Fashion Intelligence extracts structured insight from that noise. It connects to NewsAPI to pull recent English-language articles for selected luxury brands, applies a lightweight keyword-based sentiment classifier, and surfaces three analytical views:

1. **Ranking** — which brand has the strongest positive-to-negative ratio right now
2. **Composition** — how positive, neutral, and negative articles break down per brand
3. **Correlation** — whether higher article volume correlates with better sentiment

The entire pipeline runs in a single Python environment with no external database or cloud service required. It is designed for reproducibility: anyone can clone the repo, add a free NewsAPI key, and generate fresh results in under a minute.

## Features

- Live data fetching from NewsAPI with cache management
- Sentiment ranking with tiered color coding
- Article breakdown (positive / neutral / negative)
- Volume vs. sentiment scatter plot
- CSV export for further analysis
- Fallback dataset — works without API key

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
