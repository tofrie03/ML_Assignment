import pandas as pd

pd.set_option("display.max_columns", None)

# CSV URLs
price_csv = "https://raw.githubusercontent.com/tofrie03/ML_Assignment/refs/heads/main/exports/price_spain.csv"
production_csv = "https://raw.githubusercontent.com/tofrie03/ML_Assignment/refs/heads/main/exports/production_spain.csv"

# Read CSVs
df_price = pd.read_csv(price_csv, sep=",", parse_dates=["datetime"])
df_production = pd.read_csv(production_csv, sep=",", parse_dates=["Hour"])

# Adjust column name for join
df_production = df_production.rename(columns={"Hour": "datetime"})

# Remove time zones if present
df_price["datetime"] = pd.to_datetime(df_price["datetime"], utc=True).dt.tz_localize(None)
df_production["datetime"] = pd.to_datetime(df_production["datetime"])

# Merge
df_all = pd.merge(df_price, df_production, on="datetime", how="inner")

# Add additional categorical features

# 1. Time of day category
def get_day_period(hour):
    if 0 <= hour < 6:
        return 'Night'
    elif 6 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 18:
        return 'Afternoon'
    else:
        return 'Evening'

df_all['hour'] = df_all['datetime'].dt.hour
df_all['day_period'] = df_all['hour'].apply(get_day_period)

# 2. Weekday and weekend category
df_all['weekday'] = df_all['datetime'].dt.day_name()
df_all['weekday_type'] = df_all['weekday'].apply(lambda x: 'Weekend' if x in ['Saturday', 'Sunday'] else 'Weekday')

# 3. Season based on month
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'

df_all['month'] = df_all['datetime'].dt.month_name()
df_all['season'] = df_all['datetime'].dt.month.map(get_season)

# Display result
print(df_all.head())
print(df_all.tail())
print("Shape:", df_all.shape)

df_all = df_all.drop(columns=["percentage"])

# Drop specified columns before saving
columns_to_drop = [
    "Combined cycle", "Solar thermal", "Thermal renewable", "Diesel engines",
    "Gas turbine", "Vapor turbine", "Auxiliary generation", "Cogeneration and waste",
    "hour", "weekday", "month",
    "Exportation Andorra", "Exportation Morocco", "Exportation Portugal", "Exportation France",
    "Importation France", "Importation Portugal", "Importation Morocco", "Importation Andorra"
]
df_all = df_all.drop(columns=columns_to_drop)

# Save DataFrame to CSV
df_all.to_csv("Energydata_Spain_202304-202504.csv", index=False)
print("CSV file 'Energydata_Spain_2020.csv' was created successfully.")