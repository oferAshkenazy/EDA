import pandas

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

def find_correlated_columns(cm:pandas.DataFrame):
    corr_columns=[]
    for column in cm.columns:
        for row in cm.columns:
            corr_columns.append(cm[column,row].values)

    return corr_columns


