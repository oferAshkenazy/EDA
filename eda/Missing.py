import streamlit
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def missing_values_histogram(df,st):
    data=[{column:df[column].value_counts().sum()} for column in df.columns]
    # Convert the list of dictionaries to a DataFrame
    formatted_data = pd.DataFrame([{name:count for single_data in data for name, count in single_data.items()}]).T.reset_index()
    formatted_data.columns = ['Column', 'Count']
    # Create a bar plot
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x='Column', y='Count', data=formatted_data, hue='Column',legend=False)


    # label count on top of each bar
    for index, row in formatted_data.iterrows():
        ax.text(index, row['Count'] + 10, str(row['Count']), color='black', ha="center", fontsize=10)

    # Add title and axis labels
    plt.title("Column Counts in Dataframe")
    plt.xlabel("Column")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(plt)
