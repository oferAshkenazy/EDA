import pandas as pd
import streamlit
import streamlit as st
import CorrelationMatrix as cm

def numerical_columns(df):
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


def write(st:streamlit,df:pd.DataFrame):
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

    with alerts:
        st.header ("Variable types:")
        st.write ("Numerical:", len(numerical_columns(df)))
        st.write ("Non-numerical:", len(non_numerical_cols(df).columns))
        st.write ("  >Categorical:", len(categorical_columns(df)))
        st.write ("  >String:", len(string_columns(df)))
        st.write ("  >Boolean:", len(boolean_columns(df)))
        st.write ("  >datetime :",len(datetime_columns(df)))
        st.write ("  >timedelta :",len(timedelta_columns(df)))
        st.write()
        st.write ("Total :",len(columns(df)))
        st.write ("Total size in memory KB:",memory_size(df))
        st.write ("Average record size in memory KB: ",round(memory_size(df)/len(df),2))
