import streamlit as st

import pandas as pd

import os

# ✅ Static file paths

EXCEL_PATH = "SiteMaster.xlsx"

OUTPUT_PATH = "Updated_Site_Data.xlsx"

# ✅ Load from updated file if available

load_path = OUTPUT_PATH if os.path.exists(OUTPUT_PATH) else EXCEL_PATH

df = pd.read_excel(load_path)

df.columns = df.columns.astype(str)

ask_columns = df.columns[4:]

# ✅ UI setup

st.set_page_config(page_title="📋 Site Data Updater", layout="wide")

st.title("📋 Site Data Updater")

# ✅ Step 1: Select Zone (column 4)

zones = df.iloc[:, 3].dropna().unique().tolist()

selected_zone = st.selectbox("📍 Select Zone", sorted(zones))

# ✅ Step 2: Filter rows for selected zone and check for blank entries

zone_df = df[df.iloc[:, 3] == selected_zone]

blank_rows_mask = zone_df[ask_columns].isnull().any(axis=1)

zone_df_blanks = zone_df[blank_rows_mask]

blank_site_count = len(zone_df_blanks)

st.markdown(f"🟡 **{blank_site_count} site(s)** still have missing fields in zone **'{selected_zone}'**.")

# ✅ Step 3: Work on first blank site automatically

if not zone_df_blanks.empty:

    current_site = zone_df_blanks.iloc[0]

    row_index = current_site.name  # index from main df

    st.markdown(f"🆔 **SAP Code:** {current_site[0]}")

    st.markdown(f"🏢 **Site Name:** {current_site[1]}")

    updates = {}

    for col in ask_columns:

        if pd.isna(current_site[col]):

            if "MOBILE" in col.upper():

                val = st.text_input(f"📱 Enter 10-digit mobile for '{col}'", key=col)

                if val and (not val.isdigit() or len(val) != 10):

                    st.warning(f"⚠️ '{col}' must be exactly 10 digits.")

            else:

                val = st.text_input(f"📝 {col}", key=col)

            updates[col] = val

    if st.button("✅ Submit"):

        # ✅ Validate all mobile fields

        mobile_invalid = any(

            "MOBILE" in col.upper() and val and (not val.isdigit() or len(val) != 10)

            for col, val in updates.items()

        )

        if mobile_invalid:

            st.error("❌ Invalid mobile number(s). Please correct and submit again.")

        else:

            for col, val in updates.items():

                df.at[row_index, col] = val if val.strip() != "" else None

            df.to_excel(OUTPUT_PATH, index=False)

            st.success("✅ Record saved! Moving to next site...")

            st.rerun()

else:

    st.info("✅ All sites in this zone are updated!")

# ✅ Always visible download button

st.markdown("---")

if os.path.exists(OUTPUT_PATH):

    with open(OUTPUT_PATH, "rb") as f:

        st.download_button("⬇️ Download Updated Excel", f, file_name="Updated_Site_Data.xlsx")
 