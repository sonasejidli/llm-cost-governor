import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import date
from tracker.pricing import calculate_cost
from tracker.budget import check_budget, DAILY_WARNING_LIMIT, DAILY_HARD_LIMIT

st.set_page_config(page_title="LLM Cost Governor", page_icon="💰", layout="wide")
st.title("💰 LLM Cost Governor — Dashboard")

conn = sqlite3.connect("data/usage.db")
df = pd.read_sql("SELECT * FROM usage ORDER BY timestamp", conn)

if df.empty:
    st.warning("Hələ heç bir məlumat yoxdur.")
    st.stop()

df["cost"] = df.apply(
    lambda r: calculate_cost(r["model"], r["input_tokens"], r["output_tokens"])["total_cost"], axis=1
)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"] = df["timestamp"].dt.date

budget = check_budget()
if budget["status"] == "hard_stop":
    st.error(f"🛑 {budget['message']}")
elif budget["status"] == "warning":
    st.warning(f"⚠️ {budget['message']}")
else:
    st.success(f"✅ {budget['message']}")

st.subheader("Günlük büdcə")
col_b1, col_b2 = st.columns([3, 1])
with col_b1:
    progress = min(budget["current_cost"] / DAILY_HARD_LIMIT, 1.0)
    st.progress(progress)
with col_b2:
    st.write(f"${budget['current_cost']:.6f} / ${DAILY_HARD_LIMIT}")

st.divider()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Ümumi çağırış", len(df))
col2.metric("Ümumi token", f"{df['total_tokens'].sum():,}")
col3.metric("Ümumi xərc", f"${df['cost'].sum():.6f}")
col4.metric("Orta xərc/çağırış", f"${df['cost'].mean():.6f}")
today_cost = df[df["date"] == date.today()]["cost"].sum()
col5.metric("Bu günkü xərc", f"${today_cost:.6f}")

st.divider()

st.subheader("Xərc trendi")
fig1 = px.line(df, x="timestamp", y="cost", color="model", markers=True)
fig1.add_hline(y=DAILY_WARNING_LIMIT, line_dash="dash",
               line_color="orange", annotation_text="Xəbərdarlıq limiti")
fig1.add_hline(y=DAILY_HARD_LIMIT, line_dash="dash",
               line_color="red", annotation_text="Hard stop limiti")
st.plotly_chart(fig1, use_container_width=True)

col5, col6 = st.columns(2)
with col5:
    st.subheader("Model üzrə xərc")
    model_cost = df.groupby("model")["cost"].sum().reset_index()
    fig2 = px.pie(model_cost, values="cost", names="model")
    st.plotly_chart(fig2, use_container_width=True)

with col6:
    st.subheader("Model üzrə müqayisə")
    model_stats = df.groupby("model").agg(
        cagiriş=("cost", "count"),
        ort_input=("input_tokens", "mean"),
        ort_output=("output_tokens", "mean"),
        ümumi_xərc=("cost", "sum")
    ).reset_index()
    st.dataframe(model_stats.round(2), use_container_width=True)

st.subheader("Günlük xərc")
daily = df.groupby("date")["cost"].sum().reset_index()
fig3 = px.bar(daily, x="date", y="cost", color_discrete_sequence=["#636EFA"])
fig3.add_hline(y=DAILY_HARD_LIMIT, line_dash="dash",
               line_color="red", annotation_text="Günlük limit")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Bütün çağırışlar")
st.dataframe(
    df[["timestamp", "model", "input_tokens", "output_tokens",
        "total_tokens", "cost", "prompt_preview"]],
    use_container_width=True
)

