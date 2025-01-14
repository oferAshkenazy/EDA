import pandas as pd
import GeneralStatistics as gs
from eda.GeneralStatistics import numerical_columns


def mean_column(df,column_name):
  if column_name in gs.numerical_columns(df):
    return df[column_name].mean()
  else:
    return 0

def median_column(df,column_name):
  if column_name in gs.numerical_columns(df):
    return df[column_name].median()
  else:
    return 0

def standard_deviation_column(df,column_name):
  if column_name in gs.numerical_columns(df):
    return df[column_name].std()
  else:
    return 0


def maximum_column(df,column_name):
  if column_name in gs.numerical_columns(df):
    return df[column_name].max()
  else:
    return 0

def minimum_column(df,column_name):
  if column_name in gs.numerical_columns(df):
    return df[column_name].min()
  else:
    return 0

def check_correlation(column_name,correlation):
  for item in correlation:
    if item[0].replace('_numeric','')==column_name or item[1].replace('_numeric','')==column_name:
        return True
  return False

def negative_column(df,column_name):
    if column_name in numerical_columns(df):
        return int((df[column_name] < 0).sum())
    return 0

def negative_column_per(df,column_name):
    if column_name in numerical_columns(df):
        return round((negative_column(df,column_name) / len(df[column_name])) * 100, 2)
    return 0

def column_type(df,column_name):
    type_list=list()
    if gs.check_uniform_column(df, column_name):
        type_list.append('Uniform')
    if gs.unique_column(df, column_name):
        type_list.append('Unique')
    if column_name in gs.categorical_columns(df):
        type_list.append('Category')
    if gs.zeros_column(df, column_name):
        type_list.append('Zeros')
    if column_name in gs.numerical_columns(df):
        type_list.append('Numeric')
    if column_name in gs.boolean_columns(df):
        type_list.append('Boolean')
    if column_name in gs.datetime_columns(df):
        type_list.append('Datetime')

    if len(type_list)==0:
        type_list.append('Text')

    return type_list

def analyze_column(df, column_name,hcm):
    result = {
        'Types': column_type(df,column_name),
        'Uniform':gs.check_uniform_column(df,column_name),
        'Unique': gs.unique_column(df,column_name),
        'Unique Count': df[column_name].nunique(),  # Count of unique values
        'Unique %': round(df[column_name].nunique() / df[column_name].value_counts().sum() * 100,2),  # Percentage of unique values
        'Missing': bool(df[column_name].isnull().any()),  # Check for missing values
        'Missing %': df[column_name].isnull().sum() / len(df) * 100,  # Percentage of missing values
        'Missing Count': int(df[column_name].isnull().sum()),  # Count of missing values
        'Mean': mean_column(df,column_name),  # Mean value
        'Median': median_column(df,column_name),  # Median value
        'Minimum': float(minimum_column(df,column_name)),  # Minimum value
        'Maximum': float(maximum_column(df,column_name)),  #data st Maximum value
        'Standard Deviation': round(standard_deviation_column(df,column_name),2),  # Standard deviation
        'Zeros': int((df[column_name] == 0).sum()),
        'Zeros %': round(((df[column_name] == 0).sum() / len(df[column_name])) * 100,2),
        'Negative':negative_column(df,column_name),
        'Negative %': negative_column_per(df,column_name),
        'Is Text': df[column_name].dtype == 'object' or pd.api.types.is_string_dtype(df[column_name]),  # Check if column is text
        'High Correlation': check_correlation(column_name,hcm)
    }

    return result

