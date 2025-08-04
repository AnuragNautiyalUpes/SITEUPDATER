import streamlit as st

import pandas as pd

import os

# File paths

EXCEL_PATH = "D:\\TEST\\SiteMaster.xlsx"  # <- your static file

OUTPUT_PATH = "Updated_Site_Data.xlsx"

# Load or reload Excel

if not os.path.exists(EXCEL_PATH):

    st.error("Excel file not found. Please place 'SiteMaster.xlsx' in the specified path.")

    st.stop()

df = pd.read_excel(OUTPUT_PATH if os.path.exists(OUTPUT_PATH) else EXCEL_PATH)

df.columns = df.columns.astype(str)

st.set_page_config(page_title="Site Data Updater", page_icon="📝")

st.title("📋 Site Data Updater")

# Zone selection

zones = df.iloc[:, 3].dropna().unique().tolist()

selected_zone = st.selectbox("🗂️ Select Zone", sorted(zones))

# Filter for selected zone

zone_df = df[df.iloc[:, 3] == selected_zone]

ask_columns = df.columns[4:]

# Identify rows with missing values in ask columns

blank_df = zone_df[zone_df[ask_columns].isnull().any(axis=1)].copy()

blank_site_count = blank_df.shape[0]

st.markdown(f"🟡 **{blank_site_count} site(s)** still have missing fields in zone **'{selected_zone}'**.")

# Site dropdown: Show SAP Code - Site Name

if not blank_df.empty:

    site_options = [

        f"{row[0]} - {row[1]}" for _, row in blank_df.iterrows()

    ]

    selected_site_label = st.selectbox("✏️ Select Site (SAP - Name)", site_options)

    # Extract SAP Code from selection

    selected_sap_code = selected_site_label.split(" - ")[0]

    current_row = df[df.iloc[:, 0] == selected_sap_code]

    if not current_row.empty:

        row_index = current_row.index[0]

        current_site = current_row.iloc[0, 1]

        st.markdown(f"🆔 **SAP Code:** {selected_sap_code}")

        st.markdown(f"🏢 **Site Name:** {current_site}")

        updated_data = {}

        for col in ask_columns:

            current_val = df.at[row_index, col]

            placeholder = f"Enter value for '{col}' (optional)"

            if 'MOBILE' in col.upper():

                val = st.text_input(f"📱 {placeholder}", value='' if pd.isna(current_val) else str(current_val))

                if val and (not val.isdigit() or len(val) != 10):

                    st.error("❌ Mobile number must be exactly 10 digits.")

                    st.stop()

            else:

                val = st.text_input(f"📝 {placeholder}", value='' if pd.isna(current_val) else str(current_val))

            updated_data[col] = val.strip() if val else None

        if st.button("✅ Submit"):

            for col, val in updated_data.items():

                df.at[row_index, col] = val

            df.to_excel(OUTPUT_PATH, index=False)

            st.success("✅ Saved! Move to next site using dropdown above.")

else:

    st.info("🎉 No blank entries in this zone.")

# Always show download button

with open(OUTPUT_PATH if os.path.exists(OUTPUT_PATH) else EXCEL_PATH, "rb") as f:

    st.download_button("📥 Download Updated Excel", f, file_name="Updated_Site_Data.xlsx")
 