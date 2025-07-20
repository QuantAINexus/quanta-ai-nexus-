# pages/2_Dashboard.py
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import time
import random

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📊 Dashboard")
st.markdown("Welcome to your admin dashboard for QuantaAI Nexus!")

# Simulate data (replace with actual data fetch logic)
total_users = 128
pro_users = 37
queries_today = random.randint(100, 300)
uptime_hours = 21

# Metrics row
col1, col2, col3, col4 = st.columns(4)
col1.metric("🧑‍💻 Total Users", total_users)
col2.metric("💎 Pro Users", pro_users)
col3.metric("🔎 Queries Today", queries_today)
col4.metric("⏱️ Uptime (hrs)", uptime_hours)

style_metric_cards()

# Spacer
st.markdown("---")

# Line chart placeholder
st.subheader("Usage Overview")
chart_data = {
    "Queries": [random.randint(50, 300) for _ in range(7)],
    "New Users": [random.randint(5, 20) for _ in range(7)]
}
st.line_chart(chart_data)

# Quick access buttons
st.markdown("### 🔗 Quick Access")
st.button("📜 View History")
st.button("💳 Pro Plan Management")
