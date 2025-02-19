# imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO


# Our App Setup
st.set_page_config(page_title="📀Data Cleaner", layout="wide")
st.title("📀Data Cleaner")
st.write("This app allows you to clean your data by removing duplicates and missing values also converts your files between csv, excel.")

# Uploading the file
uploaded_file = st.file_uploader("Upload your file", type=["csv", "xlsx", "xls"] , accept_multiple_files=True)
if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx" or file_ext == ".xls":
            df = pd.read_excel(file)
        else:
            st.error(f"File type {file_ext} is unsupported")
            continue

        # Ensure df is not None before proceeding
        if df is not None:
            st.write(f"**File Name:** {file.name}")
            st.write(f"**File Size:** {file.size/1024:.2f} KB")
            st.write("Preview the head of the DataFrame")
            st.dataframe(df.head())

            st.subheader("Data Cleaning Options")
            if st.checkbox(f"Clean data for {file.name}"):
                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f"Remove Duplicates from {file.name}"):
                        df.drop_duplicates(inplace=True)
                        st.write(f"Successfully removed duplicates.")

                with col2:
                   if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write(f"Successfully filled missing values.")

        #Choose specific columns to keep or convert
        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose column for {file.name}" , df.columns , default=df.columns)
        df = df[columns]

        # Create some Visualization
        st.subheader("📊Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include=['number']).iloc[:,: 0])

        # Initialize buffer, file_name, and mime_type
        buffer = None
        file_name = None
        mime_type = None

        # File Conversion CSV --> Excel
        st.subheader("🔄File Conversion")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

        # Ensure buffer is not None before attempting to download
        if buffer is not None:
            st.download_button(
                label=f"🔽⬇Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
            