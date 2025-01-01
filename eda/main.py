from operator import index

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math
import numpy as np
import GeneralStatistics as gs
import CorrelationMatrix as cm
import ColumnStatistics as cs

st.text("choose csv file")
uploaded_file = st.file_uploader("Choose a file", type=["csv"])
df=pd.DataFrame|None
create_report=False

def get_dataframe():
    return df

def get_file():
    return uploaded_file

if uploaded_file is not None:
    # Handle CSV file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        st.write("Data from CSV file:")
        st.dataframe(df.head())
        create_report=True
else:
    st.write("No file uploaded yet!")

while create_report:

    correlation_matrix = cm.get_correlation_matrix(df)
    hcm=cm.find_correlated_columns(correlation_matrix)
    gs.write(st, df,hcm)
    st.write("Variables:")

    def process_selection(option):
        result = cs.analyze_column(df, option,hcm)
        st.write(option)
        st.write(result)

    data_dict = {column_name:column_name for column_name in gs.columns(df) if column_name.find('_numeric')<0}

    selected_option  = st.selectbox("Select a person:", list(data_dict.keys()))
    process_selection(selected_option )
    create_report=False