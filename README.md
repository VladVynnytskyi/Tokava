# AI Cost Analyzer

A web dashboard that turns your OpenAI or Claude API usage CSV into a beautiful, interactive cost report — in seconds.

![AI Cost Analyzer](https://img.shields.io/badge/Python-FastAPI-009688?style=flat-square&logo=fastapi) ![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=flat-square&logo=pandas) ![Plotly](https://img.shields.io/badge/Plotly.js-Charts-3F4F75?style=flat-square&logo=plotly)

## What it does

- **Total spend & daily trends** — see exactly where your budget goes
- **Model breakdown** — GPT-4o vs GPT-4o-mini vs Claude Sonnet vs Haiku
- **Top users & projects** — who is responsible for the most spending
- **Anomaly detection** — flags requests that cost way more than your average
- **Smart insights** — personalized tips based on your actual data
- **PDF export** — download a full report via browser print

## Supported formats

| Provider | CSV columns required |
|----------|----------------------|
| OpenAI   | `timestamp`, `model`, `input_tokens`, `output_tokens`, `total_tokens`, `cost_usd`, `project_id`, `user_id` |
| Anthropic | `timestamp`, `model`, `input_tokens`, `output_tokens`, `total_tokens`, `cost_usd`, `workspace_id`, `user_id` |

## Privacy

- Your file is processed in memory and **never stored**
- No database, no logging, no tracking
- 100% free, no sign-up required

## Run locally

```bash
# 1. Clone the repo
git clone https://github.com/VladVynnytskyi/AI_analyzer.git
cd AI_analyzer

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
uvicorn main:app --reload
```

Open [http://localhost:8000](http://localhost:8000), drop your CSV and get your dashboard.

## Project structure

```
AI_analyzer/
├── main.py          # FastAPI server — accepts CSV, returns JSON
├── analyzer.py      # Pandas logic — all calculations and anomaly detection
├── requirements.txt
└── static/
    ├── index.html   # Full frontend with Plotly.js charts
    └── style.css    # Styles and animations
```

## Tech stack

- **Backend** — Python, FastAPI, Pandas
- **Frontend** — Vanilla HTML/JS, Plotly.js
- **Deploy** — Railway
