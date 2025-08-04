import streamlit as st

import pandas as pd

import os

# 🔧 Set the path of your Excel file here

EXCEL_PATH = "SiteMaster.xlsx"

# 📦 Load data

if not os.path.exists(EXCEL_PATH):

    st.error("Excel file not found. Please place 'SiteMaster.xlsx' in the same folder.")

    st.stop()

df = pd.read_excel(EXCEL_PATH)

df.columns = df.columns.astype(str)  # ensure string column headers

st.title("📋 Site Data Updater")

# 🔍 Extract dropdown options

zones = df.iloc[:, 3].dropna().unique().tolist()  # Zone is column 4 (index 3)

selected_zone = st.selectbox("🏗️ Select Zone", zones)

# 🎯 Columns from 5th onward (index 4)

ask_columns = df.columns[4:]

# 🔍 Filter rows for selected zone with any blank values in input columns

filtered_df_all = df[df.iloc[:, 3] == selected_zone]

filtered_df = filtered_df_all[filtered_df_all[ask_columns].isnull().any(axis=1)]

st.markdown(f"🟡 **{len(filtered_df)} site(s)** still have missing fields in zone **'{selected_zone}'**.")

if not filtered_df.empty:

    # Create dropdown with SAP Code + Site Name

    filtered_df_all["combined_label"] = filtered_df_all.iloc[:, 0].astype(str) + " - " + filtered_df_all.iloc[:, 1]

    selected_label = st.selectbox("🏷️ Select Site (SAP - Name)", filtered_df_all["combined_label"])

    # Extract index of selected row

    row_index = filtered_df_all[filtered_df_all["combined_label"] == selected_label].index[0]

    current_site = df.loc[row_index]

    st.markdown(f"🆔 **SAP Code:** {current_site.iloc[0]}  \n🏢 **Site Name:** {current_site.iloc[1]}")

    # 📝 Input fields

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

    # ✅ Submit and Save

    if st.button("✅ Submit"):

        mobile_invalid = any(

            'MOBILE' in col.upper() and val and (not val.isdigit() or len(val) != 10)

            for col, val in updates.items()

        )

        if mobile_invalid:

            st.error("❌ Invalid mobile number(s). Please fix and resubmit.")

        else:

            for col, val in updates.items():

                df.at[row_index, col] = val if val != "" else None

            # Save updated Excel

            df.to_excel("Updated_Site_Data.xlsx", index=False)

            st.success("✅ Saved! Moving to next site...")

            st.rerun()

else:

    st.success(f"🎉 All sites in zone **'{selected_zone}'** are completed!")

    # 📥 Download Button

    with open("Updated_Site_Data.xlsx", "rb") as f:

        st.download_button("⬇️ Download Updated Excel", f, file_name="Updated_Site_Data.xlsx")
 