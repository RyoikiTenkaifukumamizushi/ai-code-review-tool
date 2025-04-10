import pandas as pd
def fill_missing_with_mean(df, column):
    if column in df.columns:
        df[column] = df[column].fillna(df[column].mean())
    return df
def drop_duplicates(df):
    return df.drop_duplicates()