import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Deep Sweeper", layout='wide' )

#custom css
st.markdown(
    """
    <style>
    .stApp{
        background-color: black;
        color: white;
       }
       <style/>
       """,
       unsafe_allow_html=True

)

#title and discription
st.title("Deepp sweeper sterling assignment by Sidra Haq")
st.write("Transform your data into a CVS and Excel forms with built-in data cleaning and visualization for quater3")

#file uploader
uploaded_files = st.file_uploader("Upload your CSV or Excel file", type=['csv', 'xlsx'], accept_multiple_files=(True))

if uploaded_files:
    for file in uploaded_files:
       file_ext =os.path.splitext(file.name)[-1].lower()

       if file_ext == ".CVS":
              df = pd.read_csv(file)
       elif file_ext == ".xlsx":
              df = pd.read_excel(file)
       else:
        st.error(f"unsupported file format: {file_ext}")
        continue


       #file details
       st.write("🔍 Preview the head of the Dataframe")
       st.dataframe(df.head())
       
       #data cleaning options
       st.subheader("Data Cleaning Options")
       if st.checkbox(f"clean data for {file.name}"):
           cols1 , cols2 = st.columns(2)
           
           with cols1:
               if st.button(f"Remove duplicates from file: {file.name}"):
                   df.drop_duplicates(inplace=True)
                   st.write("Duplicates removed")
       
           with cols2:
               if st.button(f"Drop missing values from file: {file.name}"):
                   numeric_cols = df.select_dtypes(include=[numbers]).columns
                   df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                   st.write("Missing values removed")        
       
           st.subheader("Select columns to keep")
           columns = st.multiselect(f"Select columns for {file.name}", df.columns , default=df.columns)
           df = df[columns]
       
       #data visualization
           st.subheader("Data Visualization")
           if st.checkbox(f"show Visualize data for {file.name}"):
               st.bar_chart(df.select_dtypes(include='numbers').iloc[:, :2])
       
       #conversiion options
       
       st.subheader("🔃Conversion Options")
       conversion_type = st.radio(f"conver {file.name} to:", ["CSV", "Excel"],key=file.name) 
       if st.button(f"Convert {file.name}"):
           if conversion_type == "CSV":
              df.to.cvs(buffer, index=False)
              file_name(file.name.replace(file_ext, ".csv"))
              mime_type = "text/csv"
       
           elif conversion_type == "Excel":
                  df.to.to_excel(buffer, index=False)
                  file_name(file.name.replace(file_ext, ".xlsx"))
                  mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                  buffer.seek(0)
           st.download_button(
                       label=f"Click to download {file.name} as {conversion_type}",
                       data=buffer,
                       file_name=file_name,
                       mime=mime_type
                     )
st.success("All done successfully! 🎉")              