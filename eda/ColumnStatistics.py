import numpy as np
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
'''
def analyze_correlation(column_name):
  correlation=list()
  for column in correlation_matrix.columns:
    if (column_name in correlation_matrix.columns):
      if (abs(correlation_matrix.loc[column_name,column])>correlation_threshold() and column!=column_name):
        correlation.append([column_name,column])

  return correlation

def print_correlation(correlation):
  text=str()
  for item in correlation:
    text+="  " + item[0].replace('_numeric','') + " has high correlation with " + item[1].replace('_numeric','')

  return text
'''
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
    type=list()
    if gs.check_uniform_column(df, column_name):
        type.append('Uniform')
    if gs.unique_column(df, column_name):
        type.append('Unique')
    if column_name in gs.categorical_columns(df):
        type.append('Category')
    if gs.zeros_column(df, column_name):
        type.append('Zeros')
    if column_name in gs.numerical_columns(df):
        type.append('Numeric')
    if column_name in gs.boolean_columns(df):
        type.append('Boolean')
    if column_name in gs.datetime_columns(df):
        type.append('Datetime')

    return type

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
        'Minimum': int(minimum_column(df,column_name)),  # Minimum value
        'Maximum': int(maximum_column(df,column_name)),  # Maximum value
        'Standard Deviation': round(standard_deviation_column(df,column_name),2),  # Standard deviation
        'Zeros': int((df[column_name] == 0).sum()),
        'Zeros %': round(((df[column_name] == 0).sum() / len(df[column_name])) * 100,2),
        'Negative':negative_column(df,column_name),
        'Negative %': negative_column_per(df,column_name),
        'Is Text': df[column_name].dtype == 'object' or pd.api.types.is_string_dtype(df[column_name]),  # Check if column is text
        'High Correlation': check_correlation(column_name,hcm)
    }

    return result


'''
    print(result)
    if (column_name in numerical_columns(df)):
      plt.figure(figsize=(4, 2))
      sns.histplot(df[column_name], kde=True)
      plt.title(column_name + " Histogram")
      plt.xlabel(column_name)

    if (column_name in categorical_columns(df)):
      plt.figure(figsize=(4, 2))
      sns.countplot(x=df[column_name])
      plt.title(column_name + " Count Plot")
'''

