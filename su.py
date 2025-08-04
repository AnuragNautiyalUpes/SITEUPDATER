import streamlit as st

import pandas as pd

import os

# ✅ Paths

EXCEL_PATH = "SiteMaster.xlsx"

OUTPUT_PATH = "Updated_Site_Data.xlsx"

# ✅ Load most recent data

load_path = OUTPUT_PATH if os.path.exists(OUTPUT_PATH) else EXCEL_PATH

df = pd.read_excel(load_path)

df.columns = df.columns.astype(str)

ask_columns = df.columns[4:]

# ✅ UI setup

st.set_page_config(page_title="📋 Site Data Updater", layout="wide")

st.title("📋 Site Data Updater")

# ✅ Step 1: Zone selection

zones = df.iloc[:, 3].dropna().unique().tolist()

selected_zone = st.selectbox("📍 Select Zone", sorted(zones))

# ✅ Step 2: Filter to selected zone + blanks only

zone_df = df[df.iloc[:, 3] == selected_zone]

blank_mask = zone_df[ask_columns].isnull().any(axis=1)

zone_blanks = zone_df[blank_mask]

blank_count = len(zone_blanks)

st.markdown(f"🟡 **{blank_count} site(s)** still have missing fields in zone **'{selected_zone}'**.")

# ✅ Step 3: Dropdown for blank sites

if not zone_blanks.empty:

    zone_blanks["Label"] = zone_blanks.iloc[:, 0].astype(str) + " - " + zone_blanks.iloc[:, 1]

    site_list = zone_blanks["Label"].tolist()

    selected_label = st.selectbox("🏷️ Select Site (SAP - Name)", site_list)

    selected_row = zone_blanks[zone_blanks["Label"] == selected_label]

    row_index = selected_row.index[0]

    current_site = df.loc[row_index]

    st.markdown(f"🆔 **SAP Code:** {current_site[0]}")

    st.markdown(f"🏢 **Site Name:** {current_site[1]}")

    updates = {}

    for col in ask_columns:

        if pd.isna(current_site[col]):

            if "MOBILE" in col.upper():

                val = st.text_input(f"📱 {col} (10-digit)", key=col)

                if val and (not val.isdigit() or len(val) != 10):

                    st.warning(f"⚠️ '{col}' must be exactly 10 digits.")

            else:

                val = st.text_input(f"📝 {col}", key=col)

            updates[col] = val

    if st.button("✅ Submit"):

        mobile_invalid = any(

            "MOBILE" in col.upper() and val and (not val.isdigit() or len(val) != 10)

            for col, val in updates.items()

        )

        if mobile_invalid:

            st.error("❌ Invalid mobile number(s). Please correct.")

        else:

            for col, val in updates.items():

                df.at[row_index, col] = val if val.strip() != "" else None

            df.to_excel(OUTPUT_PATH, index=False)

            st.success("✅ Record saved! Moving to next...")

            st.rerun()

else:

    st.info("✅ All sites updated in this zone!")

# ✅ Always visible download button

st.markdown("---")

if os.path.exists(OUTPUT_PATH):

    with open(OUTPUT_PATH, "rb") as f:

        st.download_button("⬇️ Download Updated Excel", f, file_name="Updated_Site_Data.xlsx")
 