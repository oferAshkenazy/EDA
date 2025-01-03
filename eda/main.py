import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit
import streamlit as st

import ColumnStatistics as cs
import CorrelationMatrix as cm
import GeneralStatistics as gs
import Missing as m

df=pd.DataFrame|None
create_report=False
selected_option_y=str|None
selected_option_x=str|None
original_columns=list()

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

st.text("choose csv file")
uploaded_file = st.file_uploader("Choose a file", type=["csv"])

def get_original_columns():
    return original_columns

def get_dataframe():
    return df

def get_file():
    return uploaded_file

if uploaded_file is not None:
    # Handle CSV file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        st.write("Data from CSV file:")
        st.markdown(
            df.head().to_html(classes="dataframe-table", index=False),
            unsafe_allow_html=True,
        )
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


def process_selection(option):
        result = cs.analyze_column(df, option,hcm)
        write_column_data(option,result)



# Main logic
while create_report:
    original_columns=df.columns
    correlation_matrix = cm.get_correlation_matrix(df)
    hcm = cm.find_correlated_columns(correlation_matrix)
    gs.write(st, df, hcm)
    st.write("Variables:")

    data_dict = {column_name: column_name for column_name in gs.columns(df) if "_numeric" not in column_name}

    selected_option = st.selectbox("Select a variable:", list(data_dict.keys()), key="select_variable")
    process_selection(selected_option)

    st.write("Correlations:")
    cm.display_correlation_matrix(correlation_matrix, st)

    st.write("Interactions:")

    selected_option_x = st.selectbox(
        "Select a column X:",
        list(get_original_columns()),
        key="select_x"
    )

    selected_option_y = st.selectbox(
        "Select a column Y:",
        list(get_original_columns()),
        key="select_y"
    )

    selected_option_hue = st.selectbox(
        "Select a column 'hue':",
        list(['']+[name for name in gs.categorical_columns(df) if "_numeric" not in name]),
        key="select_hue"
    )

    if st.button("Click"):
        cm.display_interactions_plot(df, st, selected_option_x, selected_option_y,selected_option_hue)

    st.write("Missing values:")
    m.missing_values_histogram(df,st)
    create_report = False
