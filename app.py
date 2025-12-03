import streamlit as st
import pandas as pd
import random
import time
import os

st.set_page_config(page_title="DVMSC Raffle", page_icon="🎰", layout="wide")

st.title("🎰 DVinci MSC Raffle System")

# Load Participant Data (NO duplicate removal)
@st.cache_data
def load_data():
    df = pd.read_excel("participants.xlsx")
    return df

# Save updated participant list
def save_data(df):
    df.to_excel("participants.xlsx", index=False)

# Load Winner History
def load_winner_history():
    if os.path.exists("winner_history.xlsx"):
        return pd.read_excel("winner_history.xlsx")
    else:
        return pd.DataFrame(columns=["CONTROL NO.", "FULL NAME", "POSITION", "REGION/SOC", "HUB"])

def save_winner_history(df):
    df.to_excel("winner_history.xlsx", index=False)

df = load_data()
winners_df = load_winner_history()

# REMOVE winners from ACTIVE LIST (based on FULL NAME)
if not winners_df.empty:
    df = df[~df["FULL NAME"].isin(winners_df["FULL NAME"])]

# 📌 LIVE PARTICIPANT LIST VIEWER (with duplicates intact)
with st.expander("📋 View Active Participants (Live List)"):
    st.dataframe(df.reset_index(drop=True), use_container_width=True)

# 📌 WINNER HISTORY LIST
with st.expander("🏆 View Winner History"):
    st.dataframe(winners_df.reset_index(drop=True), use_container_width=True)


slot_placeholder = st.empty()

# RANDOMIZER BUTTON
if st.button("🎲 Start Randomizer", use_container_width=True):

    if df.empty:
        st.error("No participants left!")
        st.stop()

    # Slot-machine rolling animation
    for _ in range(40):
        random_row = df.sample(1).iloc[0]
        slot_placeholder.markdown(
            f"""
            <h1 style='text-align:center; font-size:60px;'>
                {random_row['CONTROL NO.']}
            </h1>
            """,
            unsafe_allow_html=True
        )
        time.sleep(0.05)

    # FINAL WINNER
    winner = random_row

    st.subheader("🎉 WINNER SELECTED!")
    st.write(f"**CONTROL NO:** {winner['CONTROL NO.']}")
    st.write(f"**FULL NAME:** {winner['FULL NAME']}")
    st.write(f"**POSITION:** {winner['POSITION']}")
    st.write(f"**REGION/SOC:** {winner['REGION/SOC']}")
    st.write(f"**HUB:** {winner['HUB']}")

    # Save winner to winner_history.xlsx
    winners_df = pd.concat([winners_df, pd.DataFrame([winner])], ignore_index=True)
    save_winner_history(winners_df)

    # Remove ALL entries of winner from active list (so they cannot win again)
    df = df[df["FULL NAME"] != winner["FULL NAME"]]
    save_data(df)

    st.success("Winner removed from active list!")
