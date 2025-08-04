import streamlit as st

import pandas as pd

import os

# ✅ Static Excel paths

EXCEL_PATH = "SiteMaster.xlsx"

OUTPUT_PATH = "Updated_Site_Data.xlsx"

# ✅ Load Excel

if not os.path.exists(EXCEL_PATH):

    st.error("❌ 'SiteMaster.xlsx' not found. Place it in the same folder.")

    st.stop()

df = pd.read_excel(EXCEL_PATH)

df.columns = df.columns.astype(str)

ask_columns = df.columns[4:]

st.set_page_config(page_title="📋 Site Data Updater", layout="wide")

st.title("📋 Site Data Updater")

# ✅ Select Zone (from Column D)

zones = df.iloc[:, 3].dropna().unique().tolist()

selected_zone = st.selectbox("📍 Select Zone", sorted(zones))

# ✅ Live count of sites with missing values in E onwards

zone_df = df[df.iloc[:, 3] == selected_zone]

blank_rows_mask = zone_df[ask_columns].isnull().any(axis=1)

blank_site_count = blank_rows_mask.sum()

st.markdown(f"🟡 **{blank_site_count} site(s)** still have missing fields in zone **'{selected_zone}'**.")

# ✅ Sites with missing fields

zone_blanks = zone_df[blank_rows_mask]

if not zone_blanks.empty:

    zone_blanks["Site_Label"] = zone_blanks.iloc[:, 0].astype(str) + " - " + zone_blanks.iloc[:, 1]

    selected_label = st.selectbox("🏷️ Select Site (SAP - Name)", zone_blanks["Site_Label"])

    selected_row = zone_blanks[zone_blanks["Site_Label"] == selected_label]

    if not selected_row.empty:

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

    st.info("✅ All sites in this zone are updated.")

# ✅ Always visible download button

st.markdown("---")

if os.path.exists(OUTPUT_PATH):

    with open(OUTPUT_PATH, "rb") as f:

        st.download_button("⬇️ Download Updated Excel", f, file_name="Updated_Site_Data.xlsx")
 