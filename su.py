import streamlit as st

import pandas as pd

import os

# --- CONFIGURATION ---

st.set_page_config(page_title="📋 Site Data Updater", layout="centered")

# --- CONSTANTS ---

EXCEL_PATH = "SiteMaster.xlsx"

OUTPUT_PATH = "Updated_Site_Data.xlsx"

# --- LOAD DATA ---

if not os.path.exists(EXCEL_PATH):

    st.error("Excel file not found. Please place 'SiteMaster.xlsx' in the same folder.")

    st.stop()

df = pd.read_excel(OUTPUT_PATH if os.path.exists(OUTPUT_PATH) else EXCEL_PATH)

df.columns = df.columns.astype(str)

st.title("📋 Site Data Updater")

# --- ZONE SELECTION ---

zones = df.iloc[:, 3].dropna().unique().tolist()

selected_zone = st.selectbox("🗂️ Select Zone", sorted(zones))

# --- FILTER DATA ---

ask_columns = df.columns[4:]  # From column E onward

zone_df = df[df.iloc[:, 3] == selected_zone]

blank_sites_df = zone_df[zone_df[ask_columns].isnull().any(axis=1)]

# --- DISPLAY BLANK SITE COUNT ---

blank_site_count = len(blank_sites_df)

st.markdown(f"🟡 **{blank_site_count} site(s)** still have missing fields in zone **'{selected_zone}'**.")

if blank_site_count == 0:

    st.info("✅ All site entries in this zone are complete.")

    st.stop()

# --- SITE SELECTION ---

site_options = blank_sites_df.apply(lambda row: f"{row[0]} - {row[1]}", axis=1).tolist()

selected_site_label = st.selectbox("📝 Select Site (SAP - Name)", site_options)

# --- CURRENT SITE DATA ---

selected_site = blank_sites_df[blank_sites_df.apply(

    lambda row: f"{row[0]} - {row[1]}" == selected_site_label, axis=1)].iloc[0]

row_index = df[(df.iloc[:, 0] == selected_site[0])].index[0]  # Match on SAP code

st.markdown(f"🆔 **SAP Code:** {selected_site[0]}")

st.markdown(f"🏢 **Site Name:** {selected_site[1]}")

# --- FORM ENTRIES ---

updates = {}

for col in ask_columns:

    placeholder = "📌"

    if "mobile" in col.lower():

        new_val = st.text_input(f"📱 Enter 10-digit number for '{col}'", max_chars=10)

        if new_val and (not new_val.isdigit() or len(new_val) != 10):

            st.warning(f"⚠️ Mobile number in '{col}' must be exactly 10 digits.")

        updates[col] = new_val

    else:

        new_val = st.text_input(f"{placeholder} Enter value for '{col}' (optional)")

        updates[col] = new_val

# ---
 