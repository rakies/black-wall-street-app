import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="Black Wall Street Prop Valuation 2.0", layout="wide")
st.title("🧬 Black Wall Street Prop Valuation System 3.0")
st.markdown("**Multi-Market | Prestige Research | Live Value Engine**")

# --- User Input ---
st.sidebar.header("📝 Enter New Prop")
player = st.sidebar.text_input("Player Name")
market = st.sidebar.selectbox("Market", ["Points", "Rebounds", "Assists", "Turnovers"])
team = st.sidebar.text_input("Player's Team (optional)")
opponent = st.sidebar.text_input("Opponent (optional)")
book_line = st.sidebar.number_input("Book Line", min_value=0.0, step=0.1)
projection = st.sidebar.number_input("Your Projection", min_value=0.0, step=0.1)
over_odds = st.sidebar.number_input("Over Odds (decimal)", min_value=1.0, step=0.01)
under_odds = st.sidebar.number_input("Under Odds (decimal)", min_value=1.0, step=0.01)

if 'prop_data' not in st.session_state:
    st.session_state.prop_data = []

if over_odds != 0 and under_odds != 0 and book_line != 0:
    implied_prob_over = round(1 / over_odds, 3)
    implied_prob_under = round(1 / under_odds, 3)

    ev_over = round((over_odds * (projection / book_line)) - 1, 3)
    ev_under = round((under_odds * (1 - (projection / book_line))) - 1, 3)

    best_bet = "Over" if ev_over > ev_under else "Under"
    edge = round(max(ev_over, ev_under) * 100, 2)
    
    st.success(f"✅ Best Bet: **{best_bet}** — Edge: **{edge}%**")
else:
    st.warning("⚠️ Please enter valid odds and a non-zero book line.")


    # Step C: Tier Tagging System
    if edge >= 25:
        tier = "🔥 Tier 1 (High Confidence)"
    elif edge >= 15:
        tier = "⚠️ Tier 2 (Moderate Confidence)"
    else:
        tier = "🧊 Tier 3 (Low Confidence)"

    st.session_state.prop_data.append({
        "Player": player,
        "Market": market,
        "Team": team,
        "Opponent": opponent,
        "Book Line": book_line,
        "Projection": projection,
        "Over Odds": over_odds,
        "Under Odds": under_odds,
        "EV Over": ev_over,
        "EV Under": ev_under,
        "Best Bet": best_bet,
        "Edge %": edge,
        "Tier": tier
    })

# --- Prop Table Display ---
if st.session_state.prop_data:
    df = pd.DataFrame(st.session_state.prop_data)
    st.subheader("📊 Prop Value Table")
    st.dataframe(df, use_container_width=True)

# --- Historical Data Fetcher ---
st.subheader("🔍 Historical Performance Lookup")
search_player = st.text_input("Enter player name for history lookup")
if st.button("Pull History"):
    if search_player:
        # Placeholder: Replace with real API integration if needed
        dates = pd.date_range(end=pd.Timestamp.today(), periods=10)
        example_stats = pd.Series([round(book_line * (0.8 + 0.05*i), 2) for i in range(10)])
        chart_df = pd.DataFrame({"Date": dates, "Stat": example_stats})
        fig = px.line(chart_df, x="Date", y="Stat", title=f"Last 10 Games: {search_player} - {market}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please enter a player name to fetch historical data.")

# Scroll fix note (Replit preview sometimes cuts height)
st.markdown("""
<style>
  .block-container {
    padding-top: 2rem;
    overflow-y: scroll;
    max-height: 90vh;
  }
</style>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("🧬 Engineered by You + ChatGPT • Black Wall Street Business")
