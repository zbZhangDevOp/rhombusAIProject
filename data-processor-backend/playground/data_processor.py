import pandas as pd
from dateutil import parser


def infer_and_convert_data_types(file_path):

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        raise ValueError(
            "Unsupported file format. Only CSV and Excel files are supported."
        )

    for col in df.columns:
        original_data = df[col].dropna()

        # Attempt to convert to numeric
        numeric_converted = pd.to_numeric(original_data, errors="coerce")
        if (
            numeric_converted.notna().mean() > 0.5
        ):  # Over half the data could be numeric
            df[col] = numeric_converted
            continue

        # Attempt to convert non-standard numeric formats
        try:
            df_non_standard_num = (
                df[col]
                .replace("[\$,]", "", regex=True)
                .apply(pd.to_numeric, errors="coerce")
            )
            if df_non_standard_num.notna().mean() > 0.5:
                df[col] = df_non_standard_num
                continue
        except ValueError:
            pass

        # Attempt to convert to datetime using multiple known formats plus a general attempt
        datetime_converted = pd.to_datetime(
            original_data, errors="coerce", infer_datetime_format=True
        )
        if datetime_converted.notna().mean() > 0.5:
            df[col] = datetime_converted
            continue

        # Known non-standard date formats
        known_date_formats = [
            "%d-%m-%Y",
            "%m-%d-%Y",
            "%Y/%m/%d",
            "%m/%d/%Y",
            "%d/%m/%Y %H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
        ]  # Add or adjust formats as necessary
        for date_format in known_date_formats:
            datetime_converted = pd.to_datetime(
                original_data, errors="coerce", format=date_format
            )
            if datetime_converted.notna().mean() > 0.5:
                df[col] = datetime_converted
                break

        if df[col].dtype == "datetime64[ns]":
            continue

        # Attempt to convert to timedelta
        try:
            timedelta_converted = pd.to_timedelta(
                original_data, unit="h", errors="coerce"
            )
            if timedelta_converted.notna().mean() > 0.5:
                print(timedelta_converted)
                df[col] = timedelta_converted
                continue
        except ValueError:
            pass

        # Complex numbers conversion
        try:
            complex_converted = original_data.apply(
                lambda x: (
                    complex(x.replace("i", "j"))
                    if isinstance(x, str) and "i" in x
                    else x
                )
            )
            if complex_converted.apply(lambda x: isinstance(x, complex)).mean() > 0.5:
                df[col] = complex_converted
                continue
        except ValueError:
            pass

        # Final generic parser as last resort for dates
        if df[col].dtype == object:
            try:
                df[col] = original_data.apply(parser.parse)
            except (ValueError, TypeError, parser._parser.ParserError):
                pass

        # Boolean conversion
        if original_data.nunique() <= 2:
            unique_values = original_data.unique()
            if set(unique_values).issubset(
                {"True", "False", "true", "false", 1, 0, "1", "0"}
            ):
                df[col] = original_data.astype(bool)
                continue

        # Set to category if still object and not many unique values
        if df[col].dtype == object and (
            original_data.nunique() / len(original_data) < 0.5
        ):
            df[col] = pd.Categorical(original_data)

    return df
