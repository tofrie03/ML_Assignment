import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn import datasets

# 1️⃣ Daten laden (Iris-Datensatz als Beispiel)
iris = datasets.load_iris()
X = iris.data  # Merkmale
y = iris.target  # Zielwerte (Kategorien der Blumen)

# 2️⃣ Aufteilen in Trainings- und Testdaten
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3️⃣ Modell erstellen und trainieren
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4️⃣ Vorhersagen treffen
y_pred = model.predict(X_test)

# 5️⃣ Evaluierung
genauigkeit = accuracy_score(y_test, y_pred)
print(f"Genauigkeit des Modells: {genauigkeit:.2f}")
print("Klassifikationsbericht:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))

# 6️⃣ Feature-Wichtigkeit visualisieren
feature_importances = model.feature_importances_
plt.bar(iris.feature_names, feature_importances)
plt.xlabel("Merkmale")
plt.ylabel("Wichtigkeit")
plt.title("Feature Importance im Random Forest")
plt.xticks(rotation=45)
plt.show()
