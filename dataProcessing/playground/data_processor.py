
import pandas as pd
from dateutil import parser

def infer_and_convert_data_types(file_path):
    
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        # Raise an error if the file format is not supported
        raise ValueError("Unsupported file format. Only CSV and Excel files are supported.")

    for col in df.columns:
        df_converted = pd.to_numeric(df[col], errors='coerce')
        if not df_converted.isna().all():  # If at least one value is numeric
            df[col] = df_converted
            continue

        # Attempt to convert to datetime
        try:
            df[col] = pd.to_datetime(df[col])
            continue
        except (ValueError, TypeError):
            pass

        # Attempt to parse non-standard date formats
        try:
            df[col] = df[col].apply(parser.parse)
            continue
        except (ValueError, TypeError, parser._parser.ParserError):
            pass

        # Attempt to convert to boolean
        unique_values = df[col].dropna().unique()
        if set(unique_values).issubset({'True', 'False', 'true', 'false'}):
            df[col] = df[col].astype(bool)
            continue

        # Check if the column should be categorical
        if len(df[col].unique()) / len(df[col]) < 0.5:  # Example threshold for categorization
            df[col] = pd.Categorical(df[col])

    return df

