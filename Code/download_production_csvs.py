from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time
import os
from datetime import datetime, timedelta

# Zeitraum für den CSV-Download festlegen
start_fetch = "2021-05-13"
end_fetch = "2025-04-01"

# old_time = 15.30 # Head

# Zeitmessung starten
start_time = time.time()

# Pfad zum Download-Verzeichnis
download_dir = os.path.abspath("downloads")

export_dir = os.path.abspath("exports")

# Chrome-Optionen konfigurieren
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# Starte den WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

initials_set = False

def download_csv(date):
    global initials_set
    # Webseite öffnen
    driver.get(f"https://demanda.ree.es/visiona/peninsula/nacionalau/tablas/{date}/2")


    if not initials_set:
        # Cookie-Banner akzeptieren
        try:
            accept_cookies = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Permitir todas las cookies')]"))
            )
            accept_cookies.click()
            print("Cookies akzeptiert.")
        except Exception as e:
            print("Cookie-Banner konnte nicht entfernt werden:", e)

        # Drei-Punkte-Menü öffnen
        try:
            menu_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.md-icon-button.menu_share.md-button.md-ink-ripple"))
            )
            menu_button.click()
            print("Menü-Button erfolgreich geklickt.")
        except Exception as e:
            print("Menü-Button konnte nicht geklickt werden:", e)

        # Sprache auf Englisch umschalten
        try:
            toggle = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'md-thumb-container')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", toggle)
            driver.execute_script("arguments[0].click();", toggle)
            print("Sprache erfolgreich auf Englisch umgestellt.")
        except Exception as e:
            print("Sprachumschalter konnte nicht geklickt werden:", e)

        initials_set = True

    # Warte auf den spezifischen Inhalt des Generation-Tabs
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//table[@id='tabla_generacion']//span[contains(text(), 'Generation mix (MW)')]"))
        )
        print("Generation-Tabelle erfolgreich geladen.")
    except Exception as e:
        print("Generation-Tabelle konnte nicht geladen werden:", e)


    # Stelle sicher, dass die Generation-Tabelle sichtbar und aktiv ist
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'tabla-evolucion-content') and contains(., 'Generation mix')]"))
        )
        print("Generation-Tab-Inhalt vollständig sichtbar.")
    except Exception as e:
        print("Generation-Inhalt nicht sichtbar oder nicht aktiv:", e)

    # Führe die AngularJS-Funktion zur CSV-Erzeugung über den Scope des Elements aus, mit Wiederholungslogik
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            script_result = driver.execute_script("""
                var el = document.querySelector('#tabla_generacion');
                if (!el || typeof angular === 'undefined') return "retry";
                var scope = angular.element(el).scope();
                if (!scope || typeof scope.csvGeneration !== 'function') return "retry";
                scope.csvGeneration('formatTableGeneration', 'tablas.title2');
                scope.$apply();
                return "success";
            """)
            print(f"CSV-Download JavaScript-Ergebnis (Versuch {attempt + 1}): {script_result}")
            if script_result == "success":
                break
            else:
                time.sleep(1)
        except Exception as e:
            print(f"Fehler beim Ausführen von csvGeneration, Versuch {attempt + 1}: {e}")
            time.sleep(1)

def download_csv_range(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    current = start
    while current <= end:
        date_str = f"{current.year}-{current.month}-{current.day}"
        download_csv(date_str)
        current += timedelta(days=1)

# Beispielaufruf für den Zeitraum 2025-04-20 bis 2025-04-23
download_csv_range(start_fetch, end_fetch)
driver.quit()

# Prüfung, ob die Anzahl der heruntergeladenen Dateien mit dem erwarteten Zeitraum übereinstimmt
expected_files = (datetime.strptime(end_fetch, "%Y-%m-%d") - datetime.strptime(start_fetch, "%Y-%m-%d")).days + 1
actual_files = len([f for f in os.listdir(download_dir) if f.endswith(".csv")])
print(f"Erwartete Anzahl an CSV-Dateien: {expected_files}, Tatsächlich gefunden: {actual_files}")
if expected_files == actual_files:
    print("✅ Alle Dateien erfolgreich heruntergeladen.")
else:
    print("⚠️ Es fehlen Dateien. Bitte überprüfen.")


# Zeitmessung beenden und Dauer ausgeben
end_time = time.time()
print(f"Gesamtdauer: {end_time - start_time:.2f} Sekunden")

# new_time = end_time - start_time
# print(f"Die Zeitdifferenz zwischen alt und neu beträgt: {new_time - old_time:.2f} Sekunden")