import streamlit as st

import pandas as pd

import os

EXCEL_PATH = "SiteMaster.xlsx"

# Load Excel

if not os.path.exists(EXCEL_PATH):

    st.error("❌ Excel file not found. Please upload 'SiteMaster.xlsx'.")

    st.stop()

df = pd.read_excel(EXCEL_PATH)

st.title("📋 Site Data Updater")

# Select Zone

if 'Zone' not in df.columns:

    st.error("❌ 'Zone' column not found.")

    st.stop()

zones = df['Zone'].dropna().unique().tolist()

selected_zone = st.selectbox("📍 Select Zone", zones)

ask_columns = df.columns[4:]

# Track progress using session state

if 'record_index' not in st.session_state:

    st.session_state.record_index = 0

# Filter for blanks

filtered_df_all = df[(df['Zone'] == selected_zone) & (df[ask_columns].isnull().any(axis=1))]

if len(filtered_df_all) == 0:

    st.success(f"🎉 All entries filled for zone '{selected_zone}'!")

    with open("Updated_Site_Data.xlsx", "rb") as f:

        st.download_button("⬇️ Download Final Updated Excel", f, file_name="Updated_Site_Data.xlsx")

    st.stop()

else:

    st.warning(f"⚠️ {len(filtered_df_all)} site(s) still have missing fields in zone '{selected_zone}'.")

# Pick site by session index

if st.session_state.record_index < len(filtered_df_all):

    current_site = filtered_df_all.iloc[st.session_state.record_index]

    row_index = current_site.name

    # Show site details

    sap = current_site.get("SAP Code", "N/A")

    name = current_site.get("Site Name", "N/A")

    st.markdown(f"### 🏗️ Site: `{sap} - {name}`")

    updates = {}

    for col in ask_columns:

        if pd.isna(df.loc[row_index, col]):

            updates[col] = st.text_input(f"📝 Enter value for '{col}' (optional)", key=col)

    if st.button("✅ Submit"):

        for col, val in updates.items():

            df.at[row_index, col] = val if val != "" else None

        # Save the Excel

        df.to_excel("Updated_Site_Data.xlsx", index=False)

        # Move to next record

        st.session_state.record_index += 1

        st.success("✅ Saved! Showing next site...")

        st.experimental_rerun()

else:

    st.success("🎉 All entries visited. Thank you!")

    with open("Updated_Site_Data.xlsx", "rb") as f:

        st.download_button("⬇️ Download Updated Excel", f, file_name="Updated_Site_Data.xlsx")
 