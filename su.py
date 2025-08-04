import streamlit as st
import pandas as pd
import os
# ✅ Static path to Excel file (no front-end upload)
EXCEL_PATH = "SiteMaster.xlsx"
OUTPUT_PATH = "Updated_Site_Data.xlsx"
# ✅ Check if file exists
if not os.path.exists(EXCEL_PATH):
   st.error("❌ Excel file not found. Please place 'SiteMaster.xlsx' in the current folder.")
   st.stop()
# ✅ Load data
df = pd.read_excel(EXCEL_PATH)
ask_columns = df.columns[4:]  # Columns E onwards
# ✅ UI
st.title("📋 Site Data Updater")
# ✅ Step 1: Select Zone from column 4 (D)
zones = df.iloc[:, 3].dropna().unique().tolist()
selected_zone = st.selectbox("📍 Select Zone", sorted(zones))
# ✅ Filter by Zone
zone_df = df[df.iloc[:, 3] == selected_zone]
# ✅ Identify blank rows in the asking columns
blank_rows = zone_df[ask_columns].isnull().any(axis=1)
blank_site_count = blank_rows.sum()
st.markdown(f"🟡 **{blank_site_count} site(s)** still have missing fields in zone **'{selected_zone}'**.")
# ✅ Show only sites with missing data
filtered_df = zone_df[blank_rows]
if not filtered_df.empty:
   site_display = filtered_df.apply(lambda row: f"{row[0]} - {row[1]}", axis=1).tolist()
   selected_site = st.selectbox("✏️ Select Site (SAP - Name)", site_display)
   # ✅ Get selected row
   selected_row = filtered_df[filtered_df.apply(lambda row: f"{row[0]} - {row[1]}", axis=1) == selected_site]
   if not selected_row.empty:
       row_index = selected_row.index[0]
       current_site = df.loc[row_index]
       st.markdown(f"🆔 **SAP Code:** {current_site[0]}")
       st.markdown(f"🏗️ **Site Name:** {current_site[1]}")
       updates = {}
       for col in ask_columns:
           existing_val = current_site[col]
           placeholder = f"Enter value for '{col}' (optional)"
           if "MOBILE" in col.upper():
               new_val = st.text_input(f"📱 {placeholder}", value="" if pd.isna(existing_val) else str(existing_val))
               if new_val and not (new_val.isdigit() and len(new_val) == 10):
                   st.warning(f"🚫 Invalid 10-digit mobile number for field: {col}")
                   st.stop()
           else:
               new_val = st.text_input(f"📝 {placeholder}", value="" if pd.isna(existing_val) else str(existing_val))
           updates[col] = new_val
       if st.button("✅ Submit"):
           for col, val in updates.items():
               df.at[row_index, col] = val if val.strip() != "" else None
           df.to_excel(OUTPUT_PATH, index=False)
           st.success("✅ Saved! Moving to next site...")
           st.rerun()
else:
   st.info("✅ No blank entries in this zone.")
# ✅ Always show download button
with open(OUTPUT_PATH, "rb") as f:
   st.download_button("⬇️ Download Updated Excel", f, file_name="Updated_Site_Data.xlsx")