import pandas as pd
import streamlit
import streamlit as st
import CorrelationMatrix as cm
from scipy.stats import kstest

def zeros_column(df:pd.DataFrame,column_name):
    return (df[column_name] == 0).any()

def zeros_column_sum(df:pd.DataFrame,column_name):
    return (df[column_name] == 0).sum()

def zeros_column_per(df:pd.DataFrame,column_name):
    return round((df[column_name] == 0).sum()/len(df)*100,2)

def unique_column(df:pd.DataFrame,column_name):
    return df[column_name].nunique() == len(df)

def numerical_columns(df):
  return [column for column in df.select_dtypes(include='number').columns.tolist() if df[column].nunique() > cm.unique_threshold_column()]

def numerical_columns_from_origin(df):
  return [column for column in df.select_dtypes(include='number').columns.tolist() if df[column].nunique() > cm.unique_threshold_column()]

def string_columns(df):
  return [column for column in df.select_dtypes(include=['object', 'string']).columns.tolist() if df[column].nunique() > cm.unique_threshold_column()]

def categorical_columns(df):
  cat_columns = df.select_dtypes(include=['category']).columns.tolist()
  inferred_categorical = [column for column in df.select_dtypes(include=['object','number']).columns if df[column].nunique() < cm.unique_threshold_column()]
  return cat_columns + inferred_categorical

def boolean_columns(df):
  return df.select_dtypes(include='bool').columns.tolist()

def datetime_columns(df):
  return df.select_dtypes(include=['datetime']).columns.tolist()

def timedelta_columns(df):
  return df.select_dtypes(include=['timedelta']).columns.tolist()

def non_numerical_cols(df):
    return df.select_dtypes(exclude='number')
def missing_cells(df):
    return df.isnull().sum().sum()

def memory_size(df):
    return df.memory_usage(deep=True).sum()/1024

def columns(df):
    return df.columns

def duplicate_rows(df):
    return df.duplicated().sum()

def write_correlation_matrix_cells(st:streamlit, hcm):
    for i in range(len(hcm)):
        st.write(hcm[i][0].replace('_numeric','') + ' is highly overall correlated with ' + hcm[i][1].replace('_numeric',''))

def write_missing_values(st:streamlit,df):
    for column in df.columns:
        if df[column].isna().sum()>0:
            st.write(column + ' has ' + str(df[column].isna().sum()) + '('+str(round(df[column].isna().sum()/len(df)*100,2))+'%)' + ' missing values')

def check_uniform_column(df:pd.DataFrame,column_name):
    if column_name not in numerical_columns(df):
        return False
    # Statistical Test for Uniform Distribution
    # Normalize column_name to [0, 1] for the uniformity test
    normalized_data = (df[column_name] - df[column_name].min()) / (
                df[column_name].max() - df[column_name].min())

    # Perform Kolmogorov-Smirnov test for uniform distribution
    stat, p_value = kstest(normalized_data, 'uniform')

    # Check if the distribution is uniform
    if p_value > 0.05:
        return True
    else:
        return False

def write(st:streamlit,df:pd.DataFrame,hcm:pd.DataFrame):
    st.markdown(
        "<h1 style='font-size: 50px; text-align: center; color: black;'>Overview</h1>",
        unsafe_allow_html=True
    )
    #st.title("Overview")

    statistics, alerts = st.tabs(["Dataset Statistics", "Alerts"])

    with statistics:
        st.header("Dataset statistics :")
        st.write("Number of columns :",len(columns(df)))
        st.write("Number of rows :",len(df))
        st.write("Missing cells :",missing_cells(df))
        st.write("Missing cells (%) :",round(missing_cells(df)/df.size*100,2))
        st.write("Duplicate rows :",duplicate_rows(df))
        st.write("Duplicate rows %:",round(duplicate_rows(df)/len(df),2))

        st.header("Variable types:")
        st.write("Numerical:", len(numerical_columns(df)))
        st.write("Categorical:", len([column_name for column_name in categorical_columns(df) if '_numeric' not in column_name]))
        st.write("Text:", len(string_columns(df)))
        st.write("Boolean:", len(boolean_columns(df)))
        st.write("Datetime :", len(datetime_columns(df)))
        st.write("Timedelta :", len(timedelta_columns(df)))
        st.write()
        st.write("Total :",len([column_name for column_name in columns(df) if '_numeric' not in column_name]))
        st.write("Total size in memory KB:", memory_size(df))
        st.write("Average record size in memory KB: ", round(memory_size(df) / len(df), 2))

    with alerts:
        write_correlation_matrix_cells(st,hcm)
        write_missing_values(st,df)
        [st.write(column_name+ ' is uniformly distributed') for column_name in numerical_columns(df) if check_uniform_column(df,column_name)]
        [st.write(column_name+ ' has unique values') for column_name in columns(df) if unique_column(df,column_name)]
        [st.write(column_name+ ' has '+ str(zeros_column_sum(df,column_name)) + ' ('+ str(zeros_column_per(df,column_name))  +') Zeros') for column_name in numerical_columns(df) if zeros_column(df,column_name)]

