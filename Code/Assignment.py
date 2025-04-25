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

def analyse_and_clean_data():
    try:
        print(df)

        # Nicht benötigte Import-/Export-Spalten entfernen
        columns_to_drop = [
            "Exportation Andorra", "Exportation Morocco", "Exportation Portugal", "Exportation France",
            "Importation France", "Importation Portugal", "Importation Morocco", "Importation Andorra"
        ]
        df.drop(columns=[col for col in columns_to_drop], inplace=True)

        # Prüfe die Datentypen aller Spalten
        print("Datentypen aller Spalten:\n", df.dtypes)

        # Auf fehlende Werte prüfen
        missing = df.isnull().sum()
        print("Fehlende Werte pro Spalte:\n", missing)

        # Keine fehlenden Werte gefunden

        # Duplikate indentifizieren und entfernen
        duplicates = df.duplicated().sum()
        print(f"Anzahl Duplikate: {duplicates}")

        df.drop_duplicates(inplace=True)

        print("Datenbereinigung abgeschlossen.")

    except Exception as e:
        print("Fehler bei der Datenbereinigung:", e)
        

def explore_data():
    try:
        # datetime-Spalte in datetime-Objekte umwandeln
        df['datetime'] = pd.to_datetime(df['datetime'])

        # Zeitreihe der Energiequellen anzeigen
        energy_sources = ['Wind', 'Nuclear', 'Coal', 'Combined cycle', 'Solar PV', 'Hydro']

        plt.figure(figsize=(14, 6))
        for src in energy_sources:
            plt.plot(df['datetime'], df[src], label=src, alpha=0.7)
        plt.title("Zeitverlauf der Energieerzeugung")
        plt.xlabel("Datum")
        plt.ylabel("Leistung (MW)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # Scatterplot: Energieerzeugung vs. Strompreis (value)
        plt.figure(figsize=(10, 6))
        plt.scatter(df['Combined cycle'], df['value'], alpha=0.5)
        plt.title("Zusammenhang zwischen Combined Cycle und Strompreis")
        plt.xlabel("Combined cycle (MW)")
        plt.ylabel("Strompreis (€/MWh)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # Korrelationsmatrix aller numerischen Spalten
        numeric_df = df.select_dtypes(include='number')
        corr = numeric_df.corr()
        plt.figure(figsize=(14, 10))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
        plt.title("Korrelationsmatrix der numerischen Merkmale")
        plt.tight_layout()
        plt.show()

        # Mapping einer kategorialen Spalte in numerisch (als Beispiel: day_period)
        df['day_period_numeric'] = df['day_period'].map({
            'Night': 0, 'Morning': 1, 'Afternoon': 2, 'Evening': 3
        })

        # Auswahl der Spalten für das Pairplot
        pairplot_columns = ['value', 'Wind', 'Nuclear', 'Coal', 'Combined cycle', 'Solar PV', 'day_period_numeric']
        sns.pairplot(df[pairplot_columns], hue='day_period_numeric', palette='Set2')
        plt.suptitle("Pairplot zur Analyse von Attributbeziehungen", y=1.02)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print("Fehler bei der explorativen Analyse:", e)


analyse_and_clean_data()

explore_data()

print(df)