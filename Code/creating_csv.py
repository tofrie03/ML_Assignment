import requests
import pandas as pd
from datetime import datetime, timedelta
# import json
# # %pip install openpyxl
# import openpyxl

def fetch_data(start_date, end_date):
    url = 'https://apidatos.ree.es/en/datos/mercados/precios-mercados-tiempo-real'
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'time_trunc': 'hour'
    }
    headers = {
        "Accept": "application/json;",
        "Content-Type": "application/json",
        "Host": "apidatos.ree.es",
        "User-Agent": "Python/3.11 requests/2.31.0"
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        values = response.json()['included'][0]['attributes']['values']
        df = pd.DataFrame(values)
        # df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
        df['value'] = df['value'].astype(float)
        return df
    else:
        print(f"Fehler bei {start_date} bis {end_date}: {response.status_code}")
        return pd.DataFrame()


# Gesamter Zeitraum
start = datetime(2024, 1, 1)
end = datetime(2025, 4, 1)

# Liste aller Zeitabschnitte a 25 Tage
step = timedelta(days=25)
date_ranges = []

current = start
while current < end:
    range_start = current
    range_end = min(current + step, end)
    date_ranges.append((range_start, range_end))
    current = range_end

# Daten sammeln
all_data = pd.DataFrame()
for s, e in date_ranges:
    print(f"Hole Daten von {s.date()} bis {e.date()}...")
    df = fetch_data(s.isoformat(), e.isoformat())
    all_data = pd.concat([all_data, df], ignore_index=True)

# Ergebnisse anzeigen
print(all_data)

# Datetime-Spalte richtig konvertieren und Zeitzone entfernen
# all_data['datetime'] = pd.to_datetime(all_data['datetime'], utc=True)
# all_data['datetime'] = all_data['datetime'].dt.tz_localize(None)

# Jetzt in csv speichern
all_data.to_csv(f"strompreise_spanien_{start}-{end}.csv", index=False)
print("Datei wurde erfolgreich gespeichert.")