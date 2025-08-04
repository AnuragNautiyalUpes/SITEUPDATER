import streamlit as st
import pandas as pd
import os
# Excel file name (must be in same GitHub repo as this script)
EXCEL_PATH = "SiteMaster.xlsx"
# Check if file exists
if not os.path.exists(EXCEL_PATH):
   st.error("❌ Excel file not found. Please upload 'SiteMaster.xlsx' to the repo.")
   st.stop()
# Load Excel
df = pd.read_excel(EXCEL_PATH)
# UI Title
st.title("📋 Site Data Updater")
# Extract zone list (from column D – index 3)
zones = df.iloc[:, 3].dropna().unique().tolist()
selected_zone = st.selectbox("📍 Select Zone", zones)
# Define columns E onward as input columns
ask_columns = df.columns[4:]
# Filter rows with selected zone and missing fields in E onward
filtered_df = df[(df['Zone'] == selected_zone) & (df[ask_columns].isnull().any(axis=1))]
# Show count of such entries
if filtered_df.empty:
   st.success("✅ No blank entries in this zone.")
else:
   st.warning(f"⚠️ {len(filtered_df)} site(s) have blank entries.")
   # Combine SAP Code and Site Name for display
   site_ids = filtered_df.iloc[:, 0].astype(str) + " - " + filtered_df.iloc[:, 1]
   selected_label = st.selectbox("🏗️ Select Site", site_ids)
   # Get the selected row index
   selected_row = filtered_df[site_ids == selected_label]
   row_index = selected_row.index[0]
   # Ask for only blank fields
   for col in ask_columns:
       if pd.isna(df.loc[row_index, col]):
           new_val = st.text_input(f"✍️ Enter value for '{col}'")
           if new_val:
               df.at[row_index, col] = new_val
   # Save + download button
   if st.button("✅ Save and Download"):
       df.to_excel("Updated_Site_Data.xlsx", index=False)
       with open("Updated_Site_Data.xlsx", "rb") as f:
           st.download_button("⬇️ Download Updated Excel", f, file_name="Updated_Site_Data.xlsx")