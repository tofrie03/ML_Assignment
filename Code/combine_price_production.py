import pandas as pd

pd.set_option("display.max_columns", None)

# CSV-URLs
price_csv = "https://raw.githubusercontent.com/tofrie03/ML_Assignment/refs/heads/main/Material/strompreise_spanien_2020-01-01%2000%3A00%3A00-2021-01-01%2000%3A00%3A00.csv"
production_csv = "https://raw.githubusercontent.com/tofrie03/ML_Assignment/refs/heads/main/Material/combined_data.csv"

# CSVs einlesen
df_price = pd.read_csv(price_csv, sep=",", parse_dates=["datetime"])
df_production = pd.read_csv(production_csv, sep=",", parse_dates=["Hour"])

# Spaltenname anpassen für Join
df_production = df_production.rename(columns={"Hour": "datetime"})

# Zeitzonen entfernen, falls vorhanden
df_price["datetime"] = pd.to_datetime(df_price["datetime"], utc=True).dt.tz_localize(None)
df_production["datetime"] = pd.to_datetime(df_production["datetime"])

# Merge
df_all = pd.merge(df_price, df_production, on="datetime", how="inner")

# Ergebnis anzeigen
print(df_all.head())
print(df_all.tail())
print("Shape:", df_all.shape)

# DataFrame in CSV speichern
df_all.to_csv("Energydata_Spain_2020.csv", index=False)
print("CSV-Datei 'Energydata_Spain_2020.csv' wurde erfolgreich erstellt.")