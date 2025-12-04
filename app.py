import streamlit as st
import pandas as pd
import random
import time
import os

st.set_page_config(page_title="DVMSC Raffle", page_icon="🎰", layout="wide")

st.title("🎰 DVinci MSC Raffle System")

# =====================================================
# UTILITIES
# =====================================================

def load_excel(file, columns=None):
    if os.path.exists(file):
        return pd.read_excel(file)
    else:
        return pd.DataFrame(columns=columns)

def save_excel(file, df):
    df.to_excel(file, index=False)

# =====================================================
# TABS
# =====================================================

tab1, tab2 = st.tabs(["🏢 Employee Raffle", "🛠 Admin Raffle"])

# =====================================================
# TAB 1 — EMPLOYEE RAFFLE
# =====================================================
with tab1:

    st.header("🏢 Employee Raffle")

    # --- RESET BUTTON ---
    if st.button("🧹 Reset EMPLOYEE Raffle"):
        # Restore participants
        if os.path.exists("original_participants.xlsx"):
            original = pd.read_excel("original_participants.xlsx")
            save_excel("participants.xlsx", original)
        else:
            st.error("Missing file: original_participants.xlsx")

        # Clear winner history
        save_excel("winner_history.xlsx",
                   pd.DataFrame(columns=["CONTROL NO.", "FULL NAME", "POSITION", "REGION/SOC", "HUB"])
        )

        st.success("Employee Raffle has been reset! Please reload the website.")
        st.stop()

    # --- LOAD DATA ---
    df = load_excel("participants.xlsx")
    winners_df = load_excel("winner_history.xlsx",
                            ["CONTROL NO.", "FULL NAME", "POSITION", "REGION/SOC", "HUB"])

    # Remove winners based on FULL NAME
    if not winners_df.empty:
        df = df[~df["FULL NAME"].isin(winners_df["FULL NAME"])]

    with st.expander("📋 View Active Participants"):
        st.dataframe(df, use_container_width=True)

    with st.expander("🏆 View Winner History"):
        st.dataframe(winners_df, use_container_width=True)

    slot_area = st.empty()

    if st.button("🎲 Start Employee Randomizer", use_container_width=True):

        if df.empty:
            st.error("No participants left!")
            st.stop()

        # Slot animation
        iterations = 120
        for i in range(iterations):
            random_row = df.sample(1).iloc[0]
            slot_area.markdown(
                f"<h1 style='text-align:center; font-size:60px;'>{random_row['CONTROL NO.']}</h1>",
                unsafe_allow_html=True
            )
            time.sleep(0.005 + (i / iterations) * 0.2)

        winner = random_row

        # Display winner
        st.subheader("🎉 WINNER SELECTED!")
        st.write(f"**CONTROL NO:** {winner['CONTROL NO.']}")
        st.write(f"**FULL NAME:** {winner['FULL NAME']}")
        st.write(f"**POSITION:** {winner['POSITION']}")
        st.write(f"**REGION/SOC:** {winner['REGION/SOC']}")
        st.write(f"**HUB:** {winner['HUB']}")

        # Save winner to history
        winners_df = pd.concat([winners_df, pd.DataFrame([winner])], ignore_index=True)
        save_excel("winner_history.xlsx", winners_df)

        # Remove from active list
        df = df[df["FULL NAME"] != winner["FULL NAME"]]
        save_excel("participants.xlsx", df)

        st.success("Winner removed from participant list!")


# =====================================================
# TAB 2 — ADMIN RAFFLE
# =====================================================

with tab2:

    st.header("🛠 Admin Raffle")

    # RESET Admin raffle only
    if st.button("🧹 Reset ADMIN Raffle"):
        if os.path.exists("original_admin.xlsx"):
            save_excel("admin.xlsx", pd.read_excel("original_admin.xlsx"))
        else:
            st.error("Missing file: original_admin.xlsx")

        save_excel("admin_winners.xlsx", pd.DataFrame(columns=["Name", "Role"]))

        st.success("Admin raffle has been fully reset! Please reload the website.")
        st.stop()

    # LOAD admin data
    admin_df = load_excel("admin.xlsx", ["Name", "Role"])
    admin_win_df = load_excel("admin_winners.xlsx", ["Name", "Role"])

    # Remove winners so they don’t get picked again
    if not admin_win_df.empty:
        admin_df = admin_df[~admin_df["Name"].isin(admin_win_df["Name"])]

    with st.expander("📋 View Admin Participants"):
        st.dataframe(admin_df, use_container_width=True)

    with st.expander("🏆 View Admin Winners"):
        st.dataframe(admin_win_df, use_container_width=True)

    slot_admin = st.empty()

    if st.button("🎲 Start Admin Randomizer", use_container_width=True):

        if admin_df.empty:
            st.error("No admin participants left!")
            st.stop()

        # Simple random animation
        iterations = 80
        for i in range(iterations):
            random_row = admin_df.sample(1).iloc[0]
            slot_admin.markdown(
                f"<h1 style='text-align:center; font-size:60px;'>{random_row['Name']}</h1>",
                unsafe_allow_html=True
            )
            time.sleep(0.01 + (i / iterations) * 0.15)

        winner = random_row

        # Show admin winner
        st.subheader("🎉 ADMIN WINNER!")
        st.write(f"**Name:** {winner['Name']}")
        st.write(f"**Role:** {winner['Role']}")

        # Save winner
        admin_win_df = pd.concat([admin_win_df, pd.DataFrame([winner])], ignore_index=True)
        save_excel("admin_winners.xlsx", admin_win_df)

        # Remove winner
        admin_df = admin_df[admin_df["Name"] != winner["Name"]]
        save_excel("admin.xlsx", admin_df)

        st.success("Admin winner removed from active list!")
