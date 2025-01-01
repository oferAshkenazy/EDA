from operator import index

import streamlit
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

def display_category_histogram(df,column_name,st:streamlit):
    # Calculate the counts of each category
    category_counts = df[column_name].value_counts().reset_index()
    category_counts.columns = [column_name, "Count"]

    # Plot the histogram for categorical data with switched axes
    plt.figure(figsize=(10, 6))
    sns.barplot(data=category_counts, x=column_name, y="Count", palette="viridis")

    # Add titles and labels
    plt.title("Histogram for Categorical Column", fontsize=16)
    plt.ylabel("Count", fontsize=14)
    plt.xlabel("Categories", fontsize=14)

    # Show the plot
    st.pyplot(plt)


def display_numeric_histogram(df,column_name,st:streamlit):
    calculated_bin= int(df[column_name].max()/20)
    if calculated_bin == 0:
        calculated_bin = 1

    bin_edges = range(int(df[column_name].min()), int(df[column_name].max()) + calculated_bin, calculated_bin)  # Bins of size 10
    df["Binned"] = pd.cut(df[column_name], bins=bin_edges, right=False)
    if calculated_bin==0:
        calculated_bin=1

    # Calculate the counts of unique values
    value_counts = df["Binned"].value_counts().reset_index()
    value_counts.columns = ["Value", "Count"]

    # Plot the counts of unique values
    plt.figure(figsize=(10, 6))
    sns.barplot(data=value_counts, x="Value", y="Count", palette="viridis")

    # Add titles and labels
    plt.title("Count of Each Unique Value in Column", fontsize=16)
    plt.xlabel("Unique Values", fontsize=14)
    plt.ylabel("Count", fontsize=14)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    # Show the plot
    st.pyplot(plt)


def write_column_data(column_name,data):
    st.write('Data for column ' + column_name)
    types=''
    for item in data['Types']:
        types+=item.upper()+' '
    st.write(types)


    if data['Unique']:
        st.write('Distinct :'+str(data['Unique Count']))
        st.write('Distinct (%):'+str(data['Unique %']))

    if data['Missing']:
        st.write('Missing :'+str(data['Missing Count']))
        st.write('Missing %:'+str(round(data['Missing %'],2)))

    st.write('Mean :'+str(data['Mean']))
    st.write('Median :'+str(data['Median']))
    st.write('Minimum :'+str(data['Minimum']))
    st.write('Maximum :'+str(data['Maximum']))
    st.write('Standard Deviation :'+str(data['Standard Deviation']))
    st.write('Zeros :'+str(data['Zeros']))
    st.write('Zeros % :'+str(data['Zeros %']))
    st.write('Negative :'+str(data['Negative']))
    st.write('Negative % :'+str(data['Negative %']))
    st.write('Is Text :'+str(data['Is Text']))
    if data['High Correlation']:
        st.write('High Correlation :'+str(data['High Correlation']))

    if column_name in gs.categorical_columns(df):
        display_category_histogram(df, column_name, st)
    elif column_name in gs.numerical_columns(df):
        display_numeric_histogram(df, column_name,st)

    #st.write(data)

while create_report:

    correlation_matrix = cm.get_correlation_matrix(df)
    hcm=cm.find_correlated_columns(correlation_matrix)
    gs.write(st, df,hcm)
    st.write("Variables:")

    def process_selection(option):
        result = cs.analyze_column(df, option,hcm)
        write_column_data(option,result)

    data_dict = {column_name:column_name for column_name in gs.columns(df) if column_name.find('_numeric')<0}

    selected_option  = st.selectbox("Select a person:", list(data_dict.keys()))
    process_selection(selected_option )

    st.write('Correlations:')
    cm.display_correlation_matrix(correlation_matrix, st)
    create_report=False