# 💰 LLM Cost Governor

A production-ready system for tracking, analyzing, and controlling LLM API costs in real time.

## Features

- **Token Tracker** — Intercepts every API call and logs token usage to SQLite
- **Cost Calculator** — Converts token counts to USD using live pricing tables
- **Budget Enforcer** — Soft warnings + hard stops when daily limits are exceeded
- **Analytics Dashboard** — Streamlit dashboard with Plotly charts
- **Smart Router** — Automatically routes prompts to cheap or expensive models based on complexity scoring

## Tech Stack

Python · OpenAI API · SQLite · Streamlit · Plotly

## Project Structure

cost_governor/
├── tracker/
│   ├── wrapper.py     # TrackerWrapper — intercepts API calls
│   ├── storage.py     # SQLite + JSONL logging
│   ├── models.py      # UsageRecord dataclass
│   ├── pricing.py     # Model pricing table
│   ├── budget.py      # Daily budget enforcement
│   └── router.py      # Cost-aware model selection
├── dashboard.py       # Streamlit analytics dashboard
├── demo.py            # Demo script
└── cost_report.py     # Terminal cost report

## Usage


from tracker.wrapper import TrackerWrapper

tracker = TrackerWrapper(auto_route=True)
response = tracker.chat([
    {"role": "user", "content": "Your question here"}
])


Run dashboard:

streamlit run dashboard.py


## How Smart Router Works

Every prompt gets a complexity score based on:
- Word count
- Keywords (analyze, compare, explain, write code...)
- Number of questions

| Score | Model | Use case |
|-------|-------|----------|
| 0-2 | gpt-4o-mini | Simple questions |
| 3-5 | gpt-4o-mini | Medium questions |
| 6+ | gpt-4o | Complex tasks |

## Results

- Tracks token usage across multiple models
- Real-time USD cost calculation
- Daily budget enforcement with hard stop
- 85%+ of simple queries routed to cheaper model
