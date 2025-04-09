def load_csv(filepath):
    import pandas as pd
    return pd.read_csv(filepath)

def summarize_data(dataframe):
    summary = {
        "columns": dataframe.columns.tolist(),
        "shape": dataframe.shape,
        "nulls": dataframe.isnull().sum().to_dict()
    }
    return summary
