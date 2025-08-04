import streamlit as st
import pandas as pd
import os
# =========================
# 🔧 CONFIGURATION
# =========================
EXCEL_PATH = "SiteMaster.xlsx"
OUTPUT_PATH = "Updated_Site_Data.xlsx"
# =========================
# 📥 LOAD EXCEL DATA
# =========================
if not os.path.exists(EXCEL_PATH):
   st.error("❌ Excel file not found. Please place 'SiteMaster.xlsx' in the same folder.")
   st.stop()
df = pd.read_excel(EXCEL_PATH)
df.columns = df.columns.astype(str)
# =========================
# 🧾 APP UI
# =========================
st.title("📋 Site Data Updater")
# Get unique Zones (column D / index 3)
zones = df.iloc[:, 3].dropna().unique().tolist()
selected_zone = st.selectbox("🏗️ Select Zone", zones)
# Columns E onward are editable
ask_columns = df.columns[4:]
# Filter records of this zone
zone_df = df[df.iloc[:, 3] == selected_zone]
# ✅ Recalculate number of blank sites live
blank_site_count = zone_df[ask_columns].isnull().any(axis=1).sum()
st.markdown(f"🟡 **{blank_site_count} site(s)** still have missing fields in zone **'{selected_zone}'**.")
# Create dropdown with SAP Code - Site Name
zone_df["combined_label"] = zone_df.iloc[:, 0].astype(str) + " - " + zone_df.iloc[:, 1]
selected_label = st.selectbox("🏷️ Select Site (SAP - Name)", zone_df["combined_label"])
# Get row index in original df
row_index = zone_df[zone_df["combined_label"] == selected_label].index[0]
current_site = df.loc[row_index]
# Display site info
st.markdown(f"🆔 **SAP Code:** {current_site.iloc[0]}  \n🏢 **Site Name:** {current_site.iloc[1]}")
# =========================
# ✍️ DATA ENTRY FORM
# =========================
updates = {}
for col in ask_columns:
   if pd.isna(current_site[col]):
       if "MOBILE" in col.upper():
           val = st.text_input(f"📱 Enter 10-digit number for '{col}'", key=f"{col}_{row_index}")
           if val and (not val.isdigit() or len(val) != 10):
               st.warning(f"⚠️ '{col}' must be exactly 10 digits.")
       else:
           val = st.text_input(f"📝 Enter value for '{col}' (optional)", key=f"{col}_{row_index}")
       updates[col] = val
# =========================
# ✅ FORM SUBMIT
# =========================
if st.button("✅ Submit"):
   # Validate mobile numbers
   mobile_invalid = any(
       "MOBILE" in col.upper() and val and (not val.isdigit() or len(val) != 10)
       for col, val in updates.items()
   )
   if mobile_invalid:
       st.error("❌ Invalid mobile number(s). Please fix and resubmit.")
   else:
       for col, val in updates.items():
           df.at[row_index, col] = val if val != "" else None
       # Save updated file
       df.to_excel(OUTPUT_PATH, index=False)
       st.success("✅ Saved! Moving to next site...")
       st.rerun()
# =========================
# 📥 ALWAYS SHOW DOWNLOAD
# =========================
st.markdown("---")
st.subheader("📂 Download Updated File")
if os.path.exists(OUTPUT_PATH):
   with open(OUTPUT_PATH, "rb") as f:
       st.download_button("⬇️ Download Updated Excel", f, file_name="Updated_Site_Data.xlsx")
else:
   st.info("ℹ️ No updates made yet. Submit at least one record to enable download.")