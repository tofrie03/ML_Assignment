import requests
import json

def fetch_data(start_date="2019-01-01", end_date="2019-01-02"):
    url = 'https://apidatos.ree.es/en/datos/balance/demanda/tiempo-real'
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
        df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
        df['value'] = df['value'].astype(float)
        return df
    else:
        print(f"Fehler bei {start_date} bis {end_date}: {response.status_code}")
        return pd.DataFrame()