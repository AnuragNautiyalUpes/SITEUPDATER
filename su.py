import streamlit as st

import pandas as pd

import os

# 🔧 Path to static Excel file

EXCEL_PATH = "SiteMaster.xlsx"

OUTPUT_PATH = "Updated_Site_Data.xlsx"

# 📦 Load data

if not os.path.exists(EXCEL_PATH):

    st.error("❌ Excel file not found. Place 'SiteMaster.xlsx' in the same folder.")

    st.stop()

df = pd.read_excel(EXCEL_PATH)

df.columns = df.columns.astype(str)  # Ensure string headers

# 🌐 UI Title

st.title("📋 Site Data Updater")

# 📍 Zone Selection

zones = df.iloc[:, 3].dropna().unique().tolist()

selected_zone = st.selectbox("🏗️ Select Zone", zones)

# 📌 Identify touchpoint columns (from 5th col onward)

ask_columns = df.columns[4:]

# 🔍 Filter incomplete sites for the selected zone

🔄 Recalculate how many are blank in current zone
current_zone_df = df[df.iloc[:, 3] == selected_zone]
blank_count = current_zone_df[ask_columns].isnull().any(axis=1).sum()
st.markdown(f"🟡 **{blank_count} site(s)** still have missing fields in zone **'{selected_zone}'**.")

# 🧠 Create combined dropdown label: SAP Code + Site Name

filtered_df_all["combined_label"] = filtered_df_all.iloc[:, 0].astype(str) + " - " + filtered_df_all.iloc[:, 1]

selected_label = st.selectbox("🏷️ Select Site (SAP - Name)", filtered_df_all["combined_label"])

# 🔎 Get selected site row

row_index = filtered_df_all[filtered_df_all["combined_label"] == selected_label].index[0]

current_site = df.loc[row_index]

# 📍 Show basic info

st.markdown(f"🆔 **SAP Code:** {current_site.iloc[0]}  \n🏢 **Site Name:** {current_site.iloc[1]}")

# ✍️ Ask for updates

updates = {}

for col in ask_columns:

    if pd.isna(current_site[col]):

        if 'MOBILE' in col.upper():

            val = st.text_input(f"📱 Enter 10-digit number for '{col}'", key=f"{col}_{row_index}")

            if val and (not val.isdigit() or len(val) != 10):

                st.warning(f"⚠️ '{col}' must be exactly 10 digits.")

        else:

            val = st.text_input(f"📝 Enter value for '{col}' (optional)", key=f"{col}_{row_index}")

        updates[col] = val

# ✅ Submit button

if st.button("✅ Submit"):

    mobile_invalid = any(

        'MOBILE' in col.upper() and val and (not val.isdigit() or len(val) != 10)

        for col, val in updates.items()

    )

    if mobile_invalid:

        st.error("❌ Invalid mobile number(s). Please fix and submit again.")

    else:

        for col, val in updates.items():

            df.at[row_index, col] = val if val != "" else None

        df.to_excel(OUTPUT_PATH, index=False)

        st.success("✅ Saved! Moving to next site...")

        st.rerun()

# 📥 Always show download button

st.markdown("---")

st.subheader("📂 Download Updated File")

if os.path.exists(OUTPUT_PATH):

    with open(OUTPUT_PATH, "rb") as f:

        st.download_button("⬇️ Download Updated Excel", f, file_name="Updated_Site_Data.xlsx")

else:

    st.info("ℹ️ No updates made yet. Submit at least one record to enable download.")
 