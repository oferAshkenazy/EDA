import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit
import streamlit as st
from numpy.matlib import empty
import numpy as np
import ColumnStatistics as cs
import CorrelationMatrix as cm
import GeneralStatistics as gs
import Missing as m

df=pd.DataFrame|None
selected_option_y=str|None
selected_option_x=str|None
original_columns=list()
seaborn_or_csv=str|None

st.markdown(
    """
    <style>
    /* Adjust the Streamlit app container */
    .block-container {
        max-width: 90%;
        padding-left: 5%;
        padding-right: 5%;
    }
    .dataframe-table {
        font-size: 12px;  /* Adjust font size */
        color: #333;      /* Optional: Text color */
        width: 100%;      /* Optional: Adjust table width */
    }
    
    /* Custom style for the active tab */
    .stTabs > .tablist > .react-tabs__tab--selected {
        background-color: #0e1117;
        color: #ffffff;
        font-family: 'Courier New', Courier, monospace;
    }
    /* Custom style for all tabs */
    .stTabs > .tablist > .react-tabs__tab {
        background-color: #e8e8e8;
        color: #4f4f4f;
        font-family: 'Courier New', Courier, monospace;
    }
    button div p {
    /* CSS styles for <p> inside a <div> */
    font-size: 18px !important;
    font-weight: bold;
    color: purple;
}
    </style>
    """,
    unsafe_allow_html=True,
)


def get_seaborn_datasets():
    try:
        sns_datasets = sns.get_dataset_names()
    except AttributeError:
        sns_datasets = []  # Fallback if the version doesn't support this
    return sns_datasets

# Load dataset based on user selection
def load_dataset(dataset_name:str):
    return sns.load_dataset(dataset_name)

def get_original_columns():
    return original_columns

def get_dataframe():
    return df

def get_file():
    return uploaded_file

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
    types = ''
    for item in data['Types']:
        types += item.upper() + ' '

    st.markdown(
        "<h1 style='font-size: 16px; text-align: center; color: white;background-color:blue;width:100%'>" + types + "</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
            "<h1 style='font-size: 16px; text-align: left; color: green;width:100%'>Data for column " + column_name + ":</h1>",
            unsafe_allow_html=True
    )



    col5,col6 = st.columns(2)

    with col5:
        #if data['Unique']:
        st.write('Distinct :'+str(data['Unique Count']))
        st.write('Distinct (%):'+str(data['Unique %']))

        if data['Missing']:
            st.write('Missing :'+str(data['Missing Count']))
            st.write('Missing %:'+str(round(data['Missing %'],2)))

        st.write('Mean :'+str(round(data['Mean'],5)))
        st.write('Median :'+str(data['Median']))
        st.write('Minimum :'+str(data['Minimum']))
        st.write('Maximum :'+str(data['Maximum']))
        st.write('Standard Deviation :'+str(data['Standard Deviation']))

    with col6:
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

def process_selection(option,hcm):
        result = cs.analyze_column(df, option,hcm)
        write_column_data(option,result)

def remove_numeric_suffix(name):
        return name.replace("_numeric", "")

def display_category_graph(df,st,colX,colY):
    fig1 = sns.catplot(data=df, x=colX, y=colY, kind='bar', errorbar='sd')
    fig1.set_titles("Average " + colX + " by " + colY + " [Error bars are std]")
    st.pyplot(fig1)

    # Scatter plot with transparency
    fig2 = sns.catplot(data=df, x=colX, y=colY, alpha=0.3)
    st.pyplot(fig2)

    # Box plot
    fig3 = sns.catplot(data=df, x=colX, y=colY, kind='box')
    st.pyplot(fig3)

    # Violin plot
    fig4 = sns.catplot(data=df, x=colX, y=colY, kind='violin')
    st.pyplot(fig4)

def create_report(df):
    st.markdown(
        df.head().to_html(classes="dataframe-table", index=False),
        unsafe_allow_html=True,
    )
    original_columns = df.columns

    correlation_matrix = cm.get_correlation_matrix(df)
    hcm = cm.find_correlated_columns(correlation_matrix)

    #Rename both columns and rows
    correlation_matrix = correlation_matrix.rename(
        columns=lambda x: remove_numeric_suffix(x),
        index=lambda x: remove_numeric_suffix(x)
    )

    st.markdown(
        "<h1 style='font-size: 30px; text-align: center; color: blue;'>Overview:</h1>",
        unsafe_allow_html=True
    )
    gs.write(st, df, hcm,original_columns)

    st.markdown(
        "<h1 style='font-size: 30px; text-align: center; color: blue;'>Variables:</h1>",
        unsafe_allow_html=True
    )
    data_dict = {column_name: column_name for column_name in gs.columns(df) if "_numeric" not in column_name}

    selected_option = st.selectbox("", list(data_dict.keys()), key="select_variable"+seaborn_or_csv)
    process_selection(selected_option,hcm)

    arr = np.array([correlation_matrix])  # Example of an empty array

    if arr.size != 0:
        st.markdown(
            "<h1 style='font-size: 30px; text-align: center; color: blue;'>Correlations:</h1>",
            unsafe_allow_html=True
        )
        cm.display_correlation_matrix(correlation_matrix, st)

    st.markdown(
        "<h1 style='font-size: 30px; text-align: center; color: blue;'>Interactions:</h1>",
        unsafe_allow_html=True
    )

    select_box_data = list(
        [original_column for original_column in original_columns if pd.api.types.is_numeric_dtype(df[original_column])])
    if len(select_box_data)>0:
        with st.spinner():
            selected_option_x = st.selectbox(
                "Select a column X:",
                select_box_data,
                key="select_x"+seaborn_or_csv
            )

            selected_option_y = st.selectbox(
                "Select a column Y:",
                select_box_data,
                key="select_y"+seaborn_or_csv
            )

        select_box_hue=list(['']+[name for name in gs.categorical_columns(df) if "_numeric" not in name and "Binned" not in name])

        with st.spinner():
                selected_option_hue = st.selectbox(
                        "Select a column 'hue':",
                        select_box_hue,
                        key="select_hue"+seaborn_or_csv
                )

        st.markdown(
            """
            <style>
            div.stButton > button {
                width: 100%;
                font-size: 16px; /* Adjust font size */
                padding: 10px; /* Adjust padding */
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        with st.spinner():
            if selected_option_x is not None and selected_option_y is not None and st.button("Execute Interactions Graph",key="EIG_"+seaborn_or_csv):
                cm.display_interactions_plot(df, st, selected_option_x, selected_option_y,selected_option_hue)

    select_box_category_data = list(
    [original_column for original_column in original_columns if pd.api.types.is_numeric_dtype(df[original_column])])

    select_box_category_columns = list(
        [name for name in gs.categorical_columns(df) if "_numeric" not in name and "Binned" not in name])


    if len(select_box_category_data)>0 and len(select_box_category_columns)>0:
        st.markdown(
            "<h1 style='font-size: 30px; text-align: center; color: blue;'>Category graphs:</h1>",
            unsafe_allow_html=True
        )

        with st.spinner():
            selected_option_cat_x = st.selectbox(
                "Select a column X:",
                select_box_category_columns,
                key="select_cat_x"+seaborn_or_csv
            )

        with st.spinner():
            selected_option_cat_y = st.selectbox(
                "Select a column Y:",
                select_box_category_data,
                key="select_cat_ y"+seaborn_or_csv
            )

        with st.spinner():
            if selected_option_cat_x is not None and st.button("Execute Category Graphs", key="ECG_" + seaborn_or_csv):
                display_category_graph(df, st, selected_option_cat_x, selected_option_cat_y)

    st.markdown(
        "<h1 style='font-size: 30px; text-align: center; color: blue;'>Missing values:</h1>",
        unsafe_allow_html=True
    )

    m.missing_values_histogram(df,st,original_columns)

seaborn_tab,csv_tab=st.tabs(["Seaborn","CSV"])

with seaborn_tab:
    st.title("Load Seaborn Datasets")

    # Dropdown to select dataset
    available_datasets = get_seaborn_datasets()
    selected_dataset = st.selectbox("Choose a Seaborn dataset to load:", available_datasets)

    if selected_dataset:
        # Load and display dataset
        with st.spinner("Loading dataset..."):
            df = load_dataset(selected_dataset)
            seaborn_or_csv='seaborn'
        st.success(f"Loaded dataset: {selected_dataset}")
        create_report(df)

with csv_tab:
    st.title(" choose csv file")
    uploaded_file = st.file_uploader("Choose a file", type=["csv"])

    if uploaded_file is not None:
        # Handle CSV file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            st.write("Data from CSV file:")
            seaborn_or_csv='csv'
            create_report(df)
    else:
        st.write("No file uploaded yet!")

