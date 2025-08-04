import streamlit as st

import pandas as pd

import os

# Define Excel file path

EXCEL_PATH = "SiteMaster.xlsx"

# Load the Excel file

if not os.path.exists(EXCEL_PATH):

    st.error("❌ Excel file not found. Please upload 'SiteMaster.xlsx' to the repo.")

    st.stop()

# Read the Excel file

df = pd.read_excel(EXCEL_PATH)

# UI Title

st.title("📋 Site Data Updater")

# Step 1: Select Zone

zones = df['Zone'].dropna().unique().tolist()

selected_zone = st.selectbox("📍 Select Zone", zones)

# Step 2: Define columns E onward for user input

ask_columns = df.columns[4:]

# Step 3: Filter for selected zone and blank fields

filtered_df = df[(df['Zone'] == selected_zone) & (df[ask_columns].isnull().any(axis=1))]

# Step 4: Show count

if filtered_df.empty:

    st.success(f"✅ No blank entries remaining in zone '{selected_zone}'!")

    with open("Updated_Site_Data.xlsx", "rb") as f:

        st.download_button("⬇️ Download Final Updated Excel", f, file_name="Updated_Site_Data.xlsx")

    st.stop()

else:

    st.warning(f"⚠️ {len(filtered_df)} site(s) still have missing fields in zone '{selected_zone}'.")

# Step 5: Show first blank site

current_site = filtered_df.iloc[0]

row_index = current_site.name  # original row index in df

st.markdown(f"### 🏗️ Site: `{current_site['SAP Code']} - {current_site['Site Name']}`")

# Step 6: Input form for blank fields

updates = {}

for col in ask_columns:

    if pd.isna(df.loc[row_index, col]):

        updates[col] = st.text_input(f"✍️ Enter value for '{col}' (optional)", key=col)

# Step 7: Submit and Save

if st.button("✅ Submit"):

    for col, val in updates.items():

        # Save as blank if left empty

        df.at[row_index, col] = val if val != "" else None

    # Save updated Excel

    df.to_excel("Updated_Site_Data.xlsx", index=False)

    # Recalculate remaining blanks

    filtered_df = df[(df['Zone'] == selected_zone) & (df[ask_columns].isnull().any(axis=1))]

    if not filtered_df.empty:

        st.success("✅ Record saved. Moving to next site...")

        st.experimental_rerun()

    else:

        st.success(f"🎉 All sites in zone '{selected_zone}' are now complete!")

        with open("Updated_Site_Data.xlsx", "rb") as f:

            st.download_button("⬇️ Download Final Updated Excel", f, file_name="Updated_Site_Data.xlsx")
 