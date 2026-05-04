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