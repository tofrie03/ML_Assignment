import requests
import pandas as pd

def fetch_production_data(start_date, end_date, geo='peninsula'):
    url = 'https://apidatos.ree.es/en/datos/generacion/estructura-generacion'

    params = {
        'start_date': start_date,
        'end_date': end_date,
        'time_trunc': 'hour',
        'geo_limit': geo
    }

    headers = {
        "Accept": "application/json;",
        "Content-Type": "application/json",
        "Host": "apidatos.ree.es",
        "User-Agent": "Python/3.11 requests/2.31.0"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        values = data['included'][0]['attributes']['values']
        df = pd.DataFrame(values)
        df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
        df['value'] = df['value'].astype(float)
        df['type'] = data['included'][0]['attributes']['type']
        return df
    else:
        print(f"Fehler bei {start_date} bis {end_date}: {response.status_code}")
        return pd.DataFrame()