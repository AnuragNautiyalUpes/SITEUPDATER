import streamlit as st
import pandas as pd
import os
# Constants
EXCEL_PATH = "SiteMaster.xlsx"
# Load Excel
if not os.path.exists(EXCEL_PATH):
   st.error("❌ Excel file not found. Please upload 'SiteMaster.xlsx' to the same folder.")
   st.stop()
df = pd.read_excel(EXCEL_PATH)
# UI Title
st.title("📋 Site Data Updater")
# Step 1: Zone selection
if 'Zone' not in df.columns:
   st.error("❌ 'Zone' column not found in Excel.")
   st.stop()
zones = df['Zone'].dropna().unique().tolist()
selected_zone = st.selectbox("📍 Select Zone", zones)
# Step 2: Ask columns from column E onward (index 4+)
ask_columns = df.columns[4:]
# Step 3: Filter zone + blanks
filtered_df = df[(df['Zone'] == selected_zone) & (df[ask_columns].isnull().any(axis=1))]
if filtered_df.empty:
   st.success(f"✅ No blank entries in zone '{selected_zone}'!")
   with open("Updated_Site_Data.xlsx", "rb") as f:
       st.download_button("⬇️ Download Final Updated Excel", f, file_name="Updated_Site_Data.xlsx")
   st.stop()
else:
   st.warning(f"⚠️ {len(filtered_df)} site(s) still have missing fields in zone '{selected_zone}'")
# Step 4: Current site
current_site = filtered_df.iloc[0]
row_index = current_site.name
# Safe get for site name/code
sap_code = current_site.get('SAP Code', 'Unknown SAP Code')
site_name = current_site.get('Site Name', 'Unknown Site')
st.markdown(f"### 🏗️ Site: `{sap_code} - {site_name}`")
# Step 5: Input form
updates = {}
for col in ask_columns:
   if pd.isna(df.loc[row_index, col]):
       updates[col] = st.text_input(f"✍️ Enter value for '{col}' (optional)", key=col)
# Step 6: Submit
if st.button("✅ Submit"):
   for col, val in updates.items():
       df.at[row_index, col] = val if val != "" else None
   df.to_excel("Updated_Site_Data.xlsx", index=False)
   # Re-filter and rerun
   filtered_df = df[(df['Zone'] == selected_zone) & (df[ask_columns].isnull().any(axis=1))]
   if not filtered_df.empty:
       st.success("✅ Saved! Moving to next site...")
       st.experimental_rerun()
   else:
       st.success(f"🎉 All sites in zone '{selected_zone}' are now complete!")
       with open("Updated_Site_Data.xlsx", "rb") as f:
           st.download_button("⬇️ Download Final Updated Excel", f, file_name="Updated_Site_Data.xlsx")