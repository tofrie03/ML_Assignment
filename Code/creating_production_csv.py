import os
import pandas as pd
from datetime import datetime

# Pfad zum Download-Verzeichnis
download_dir = os.path.abspath("downloads")

export_dir = os.path.abspath("exports")

def combine_csvs():
    # --- CSVs zusammenführen ---
    os.makedirs(export_dir, exist_ok=True)
    combined_csv_path = os.path.join(export_dir, "production_spain.csv")
    all_files = [f for f in os.listdir(download_dir) if f.endswith(".csv")]

    # Zählt die Anzahl der übersprungenen Zeilen
    loss_in_lines = 0
    # Zählt die Anzahl der zusammengeführten Zeilen
    combined_rows = 0

    combined_df = pd.DataFrame()
    for file in all_files:
        raw_date = file[14:-24]
        try:
            file_date = datetime.strptime(raw_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            try:
                file_date = datetime.strptime(raw_date, "%Y-%m-%d").date().isoformat()
            except Exception as e:
                print(f"Konnte das Datum '{raw_date}' nicht parsen: {e}")
                continue
        file_path = os.path.join(download_dir, file)
        try:
            # Entferne überflüssige Kommata am Zeilenende
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            with open(file_path, 'w', encoding='utf-8') as f:
                for line in lines:
                    if line.endswith(',\n'):
                        line = line[:-2] + '\n'
                    elif line.endswith(','):
                        line = line[:-1]
                    f.write(line)
            df = pd.read_csv(file_path, engine='python', skiprows=1, sep=',')
            print(df["Hour"])
            print(df)
            df = df[df["Hour"].astype(str).str.contains(file_date)]
            print(df)
            print(f"{file} eingelesen: {df.shape[0]} Zeilen, {df.shape[1]} Spalten")
            if df.shape[1] > 1:
                combined_df = pd.concat([combined_df, df], ignore_index=True)
                combined_rows += df.shape[0]
            else:
                print(f"{file} wurde übersprungen, da nur eine leere oder unbrauchbare Spalte vorhanden war.")
                loss_in_lines += 1
            print(combined_df.head(3))
        except Exception as e:
            print(f"Fehler beim Verarbeiten von {file}: {e}")

    print(f"Anzahl der übersprungenen Reihen: {loss_in_lines}")
    print(f"Sollwert der Zeilen: {combined_rows}, Istwert der Zeilen: {combined_df.shape[0]}")
    # Sortiere den DataFrame nach der Spalte 'Hour'
    combined_df = combined_df.sort_values(by="Hour")
    # Konvertiere 'Hour' zu datetime und filtere nur volle Stunden (Minuten == 0)
    combined_df["Hour"] = pd.to_datetime(combined_df["Hour"], errors="coerce")
    combined_df = combined_df[combined_df["Hour"].dt.minute == 0]
    combined_df.to_csv(combined_csv_path, index=False)
    print(f"Alle Dateien wurden zusammengeführt und unter {combined_csv_path} gespeichert.")

combine_csvs()