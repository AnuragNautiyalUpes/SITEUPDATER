import streamlit as st
import pandas as pd
import os
# Path to your master Excel file (relative or absolute)
EXCEL_PATH = "D:\TEST\SiteMaster.xlsx"
# Load Excel
if not os.path.exists(EXCEL_PATH):
   st.error("Excel file not found. Upload 'SiteMaster.xlsx' to this folder.")
   st.stop()
df = pd.read_excel(EXCEL_PATH)
st.title("📋 Site Data Updater")
zones = df.iloc[:, 3].dropna().unique().tolist()
selected_zone = st.selectbox("Select Zone", zones)
ask_columns = df.columns[4:]  # Columns E onward
filtered_df = df[(df.iloc[:, 3] == selected_zone) & (df[ask_columns].isnull().any(axis=1))]
if not filtered_df.empty:
   site_ids = filtered_df.iloc[:, 0].astype(str) + " - " + filtered_df.iloc[:, 1]
   selected_label = st.selectbox("Select Site", site_ids)
   selected_row = filtered_df[site_ids == selected_label]
   for col in ask_columns:
       if selected_row.iloc[0][col] in [None, ""]:
           new_val = st.text_input(f"Enter {col}", key=col)
           if new_val:
               df.loc[selected_row.index, col] = new_val
   if st.button("✅ Save and Download"):
       df.to_excel("Updated_Site_Data.xlsx", index=False)
       with open("Updated_Site_Data.xlsx", "rb") as f:
           st.download_button("⬇️ Download Excel", f, file_name="Updated_Site_Data.xlsx")
else:
   st.info("🎉 No blank entries in this zone.")