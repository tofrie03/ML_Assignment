import requests as rq
import pandas as pd
from datetime import datetime as dt, timedelta as td
import matplotlib.pyplot as plt
import seaborn as sns
import json as js

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 150)

url = "https://raw.githubusercontent.com/tofrie03/ML_Assignment/refs/heads/main/Material/Energydata_Spain_2020-2025.csv"

df = pd.read_csv(url)

def clean_data(df):
    try:
        # Nicht benötigte Import-/Export-Spalten entfernen
        columns_to_drop = [
            "Exportation Andorra", "Exportation Morocco", "Exportation Portugal", "Exportation France",
            "Importation France", "Importation Portugal", "Importation Morocco", "Importation Andorra"
        ]
        df.drop(columns=[col for col in columns_to_drop], inplace=True)

        # Prüfen ob die Datentypen aller Spalten korrekt sind
        print("Datentypen vor Cleaning:\n", df.dtypes)

        # Auf fehlende Werte prüfen
        missing = df.isnull().sum()
        print("Fehlende Werte pro Spalte:\n", missing)

        # Fehlende Werte bei numerischen Spalten mit dem Durchschnittswert auffüllen
        df.fillna(df.mean(numeric_only=True), inplace=True)

        # Duplikate indentifizieren und entfernen
        duplicates = df.duplicated().sum()
        print(f"Anzahl Duplikate: {duplicates}")

        df.drop_duplicates(inplace=True)

        print("Datenbereinigung abgeschlossen.")

    except Exception as e:
        print("Fehler bei der Datenbereinigung:", e)
        

def explore_data(df):
    try:


    except Exception as e:
        print("Fehler bei der explorativen Analyse:", e)



explore_data(df)

# clean_data(df)

# print(df)