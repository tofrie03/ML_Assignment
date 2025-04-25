import pandas as pd
from datetime import timedelta as td

test_df = pd.read_csv("test.csv")

test_df["datetime"] = pd.to_datetime(test_df["datetime"])

datetime_list = test_df["datetime"]

def calculate_next_datetime(index, row):
    try:
        if index < len(datetime_list) - 1:
            if pd.isna(row):
                next_datetime_index = index + 1
                next_datetime = datetime_list[next_datetime_index]
                if not pd.isna(next_datetime):
                    test_df[index] = next_datetime - td(hours=1)
                else:
                    calculate_next_datetime(next_datetime_index, next_datetime)
            else:
                pass
        else:
            pass
    except Exception as e:
        return e

for index, row in enumerate(datetime_list):
    try:
        calculate_next_datetime(index, row)
    except Exception as e:
        print(f"Error at index {index}: {e}")
        continue

test_df.to_csv("test_modified.csv", index=False)