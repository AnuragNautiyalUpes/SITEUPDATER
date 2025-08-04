import streamlit as st

import pandas as pd

import os

# --- CONFIGURATION ---

EXCEL_PATH = "SiteMaster.xlsx"  # Static Excel path

# --- LOAD DATA ---

if not os.path.exists(EXCEL_PATH):

    st.error("❌ Excel file not found. Please upload 'SiteMaster.xlsx'.")

    st.stop()

df = pd.read_excel(EXCEL_PATH)

st.title("📋 Site Data Updater")

# --- ZONE SELECTION ---

if 'Zone' not in df.columns:

    st.error("❌ 'Zone' column not found in Excel.")

    st.stop()

zones = df['Zone'].dropna().unique().tolist()

selected_zone = st.selectbox("📍 Select Zone", zones)

# Columns to be filled start from 5th column (i.e., index 4)

ask_columns = df.columns[4:]

# Filter all sites in zone that have blank values

filtered_df_all = df[(df['Zone'] == selected_zone) & (df[ask_columns].isnull().any(axis=1))]

# Show count of sites still pending

if len(filtered_df_all) == 0:

    st.success(f"🎉 All entries filled for zone '{selected_zone}'!")

    with open("Updated_Site_Data.xlsx", "rb") as f:

        st.download_button("⬇️ Download Final Updated Excel", f, file_name="Updated_Site_Data.xlsx")

    st.stop()

else:

    st.warning(f"⚠️ {len(filtered_df_all)} site(s) still have missing fields in zone '{selected_zone}'.")

# Track position of which site to show

if 'current_index' not in st.session_state or st.session_state.reset_zone != selected_zone:

    st.session_state.current_index = 0

    st.session_state.reset_zone = selected_zone

# All sites done

if st.session_state.current_index >= len(filtered_df_all):

    st.success("🎉 All sites reviewed in this zone!")

    with open("Updated_Site_Data.xlsx", "rb") as f:

        st.download_button("⬇️ Download Final Updated Excel", f, file_name="Updated_Site_Data.xlsx")

    if st.button("🔄 Start Over"):

        st.session_state.current_index = 0

        st.experimental_rerun()

    st.stop()

# --- CURRENT RECORD ---

current_site = filtered_df_all.iloc[st.session_state.current_index]

row_index = current_site.name

sap_code = current_site.get("SAP Code", "Unknown SAP Code")

site_name = current_site.get("Site Name", "Unknown Site")

st.markdown(f"### 🏗️ Site: `{sap_code} - {site_name}`")

# --- FORM SECTION ---

with st.form("data_entry_form", clear_on_submit=True):

    updates = {}

    mobile_invalid = False

    for col in ask_columns:

        if pd.isna(df.loc[row_index, col]):

            if 'MOBILE' in col.upper():

                updates[col] = st.text_input(f"📱 Enter 10-digit number for '{col}'", key=f"{col}_{row_index}")

                if updates[col] and (not updates[col].isdigit() or len(updates[col]) != 10):

                    st.warning(f"⚠️ '{col}' must be exactly 10 digits.")

                    mobile_invalid = True

            else:

                updates[col] = st.text_input(f"📝 Enter value for '{col}' (optional)", key=f"{col}_{row_index}")

    submitted = st.form_submit_button("✅ Submit")

    if submitted:

        if mobile_invalid:

            st.error("❌ One or more mobile numbers are invalid. Please correct them.")

        else:

            for col, val in updates.items():

                df.at[row_index, col] = val if val != "" else None

            # Save file

            df.to_excel("Updated_Site_Data.xlsx", index=False)

            st.success("✅ Saved! Moving to next site...")

            # Move to next record

            st.session_state.current_index += 1

            st.rerun()
 