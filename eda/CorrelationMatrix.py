import pandas as pd
import pandas
import streamlit
import seaborn as sns
import matplotlib.pyplot as plt
import GeneralStatistics as gs

def replace_numeric(name):
  return str(name).replace('_numeric','')

def unique_threshold_column():
    return 5

def correlation_threshold():
    return 0.5

# Used in correlation tests
def add_convertible_columns_as_numeric(df):
    max_unique = unique_threshold_column()
    non_numeric_cols = df.select_dtypes(exclude=['number']).columns

    convertible_cols = [
        col for col in non_numeric_cols if df[col].nunique() <= max_unique
    ]

    for col in convertible_cols:
        df[col + '_numeric'] = df[col].astype('category').cat.codes

    return df


def create_correlation_matrix(df):
    #df = add_convertible_columns_as_numeric(df)
    df_corr = add_convertible_columns_as_numeric(df)
    numeric_cols = df_corr.select_dtypes(include=['number'])
    return numeric_cols.corr()

def get_correlation_matrix(df):
    return create_correlation_matrix(df)

def get_matrix_cell_value(cm:pandas.DataFrame,column,row):
    return abs(cm.loc[column,row])

def find_correlated_columns(cm:pandas.DataFrame):

    corr_columns=[]

    [corr_columns.append([column,row])
        for column in cm.columns
            for row in cm.columns
                if (get_matrix_cell_value(cm,column,row)>correlation_threshold() and column!=row)]
    return corr_columns

def display_correlation_graph(st:streamlit,correlation_matrix):
    nested_list = find_correlated_columns(correlation_matrix)
    unique_list = list(dict.fromkeys(element for sublist in nested_list for element in sublist))
    pair_plot = sns.pairplot(correlation_matrix[unique_list], diag_kind="kde", corner=True, palette="viridis")
    st.pyplot(plt)

def display_correlation_matrix(correlation_matrix,st:streamlit,df):
    map, table,graphs = st.tabs(["Heat Map", "Heat Table","Graphs"])

    with map:

        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title("Correlation Matrix Heatmap")
        st.pyplot(plt)

    with table:
        st.write(correlation_matrix)

    with graphs:
        display_correlation_graph(st,correlation_matrix)
