import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 150)

url = "https://raw.githubusercontent.com/tofrie03/ML_Assignment/refs/heads/main/Material/Energydata_Spain_202304-202504.csv"

df = pd.read_csv(url)

try:
    print(df)

    # Check the data types of all columns
    print("Data types of all columns:\n", df.dtypes)

    # Check for missing values
    missing = df.isnull().sum()
    print("Missing values per column:\n", missing)

    # No missing values found

    # Identify and remove duplicates
    duplicates = df.duplicated().sum()
    print(f"Number of duplicates: {duplicates}")

    df.drop_duplicates(inplace=True)

    print("Data cleaning completed.")

except Exception as e:
    print("Error during data cleaning:", e)

# try:
#     # Convert datetime column to datetime objects
#     df['datetime'] = pd.to_datetime(df['datetime'])

#     # Show time series of energy sources
#     energy_sources = ['Wind', 'Nuclear', 'Coal', 'Solar PV', 'Hydro']

#     plt.figure(figsize=(14, 6))
#     for src in energy_sources:
#         plt.plot(df['datetime'], df[src], label=src, alpha=0.7)
#     plt.title("Time course of energy generation")
#     plt.xlabel("Date")
#     plt.ylabel("Power (MW)")
#     plt.legend()
#     plt.grid(True)
#     plt.tight_layout()
#     plt.show()

#     # Correlation matrix of all numerical columns
#     numeric_df = df.select_dtypes(include='number')
#     corr = numeric_df.corr()
#     plt.figure(figsize=(10, 8))
#     sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
#     plt.title("Correlation matrix of numerical features")
#     plt.tight_layout()
#     plt.show()

#     # Selection of columns for the pairplot
#     pairplot_columns = ['price', 'Wind', 'Nuclear', 'Coal', 'Solar PV', 'day_period']
#     g = sns.pairplot(df[pairplot_columns], hue='day_period', palette='Set2', height=1.8, aspect=1.2)
#     g.fig.suptitle("Pairplot for analysis of attribute relationships", y=1.02)

#     # Position legend outside on the right
#     g._legend.set_bbox_to_anchor((1.05, 0.5))
#     g._legend.set_loc("center left")

#     plt.tight_layout()
#     plt.show()

#     # Boxplot: Distribution of electricity price by time of day
#     plt.figure(figsize=(10, 5))
#     sns.boxplot(data=df, x='day_period', y='price', palette='Set2')
#     plt.title("Distribution of electricity price by time of day")
#     plt.ylabel("Electricity price (€/MWh)")
#     plt.xlabel("Time of day")
#     plt.grid(True)
#     plt.tight_layout()
#     plt.show()

#     # Scatterplot with threshold line
#     plt.figure(figsize=(10, 6))
#     sns.scatterplot(data=df, x='Wind', y='price', alpha=0.6)
#     plt.axhline(y=50, color='red', linestyle='--', label='Price threshold: 50 €/MWh')
#     plt.title("Wind power vs. electricity price with price threshold")
#     plt.xlabel("Wind power (MW)")
#     plt.ylabel("Electricity price (€/MWh)")
#     plt.legend()
#     plt.grid(True)
#     plt.tight_layout()
#     plt.show()

#     # Histogram of electricity prices
#     plt.figure(figsize=(10, 5))
#     sns.histplot(df['price'], bins=50, kde=True, color='skyblue')
#     plt.title("Distribution of electricity prices")
#     plt.xlabel("Price (€/MWh)")
#     plt.grid(True)
#     plt.tight_layout()
#     plt.show()

#     # Electricity price over the entire period – all individual values
#     plt.figure(figsize=(14, 6))
#     plt.plot(df['datetime'], df['price'], linestyle='-', marker='', alpha=0.6)
#     plt.title("Electricity price over the entire period")
#     plt.xlabel("Date")
#     plt.ylabel("Electricity price (€/MWh)")
#     plt.grid(True)
#     plt.tight_layout()
#     plt.show()

#     print(df)

# except Exception as e:
#     print("Error during exploratory analysis:", e)

try:
    # Rename 'value' column to 'price'
    df.rename(columns={'value': 'price'}, inplace=True)
    print(df)
    # Columns that should not be normalized
    non_numeric_cols = ['datetime', 'day_period', 'weekday_type', 'season']
    features_to_normalize = []

    for col in df.columns:
        if col not in non_numeric_cols:
            features_to_normalize.append(col)

    # Standardization
    scaler = StandardScaler()
    df[features_to_normalize] = scaler.fit_transform(df[features_to_normalize])

    print(df)
        
    df['datetime'] = pd.to_datetime(df['datetime'])
    # Extract time features from 'datetime'
    df["year"] = df["datetime"].dt.year
    df['month'] = df['datetime'].dt.month
    df['dayofweek'] = df['datetime'].dt.dayofweek
    df['hour'] = df['datetime'].dt.hour
    df.drop(columns=['datetime'], inplace=True)

    print(df)
    
    # Encode categorical columns as numeric labels
    categorical_cols = ['day_period', 'weekday_type', 'season']
    for col in categorical_cols:
        df[col] = df[col].astype('category').cat.codes

except Exception as e:
    print("Error:", e)

print(df)

# Train-test split
X = df.drop(columns=['price'])
y = df['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training data: {X_train.shape}, Test data: {X_test.shape}")

try:
    max_depth = 19

    max_depth_range = range(1, max_depth + 1)

    train_MAEs = []
    test_MAEs = []

    train_MSEs = []
    test_MSEs = []

    train_R2s = []
    test_R2s = []

    for depth in max_depth_range:
        model = RandomForestRegressor(max_depth=depth, random_state=42)
        model.fit(X_train, y_train)

        predicted_train = model.predict(X_train)
        predicted_test = model.predict(X_test)

        train_MAE = mean_absolute_error(y_train, predicted_train)
        test_MAE = mean_absolute_error(y_test, predicted_test)

        train_MSE = mean_squared_error(y_train, predicted_train)
        test_MSE = mean_squared_error(y_test, predicted_test)
        
        train_R2 = r2_score(y_train, predicted_train)
        test_R2 = r2_score(y_test, predicted_test)

        train_MAEs.append(train_MAE)
        test_MAEs.append(test_MAE)

        train_MSEs.append(train_MSE)
        test_MSEs.append(test_MSE)

        train_R2s.append(train_R2)
        test_R2s.append(test_R2)

        print(f"Depth: {depth:2} \tTrain MAE: {train_MAE:.3f} \tTest MAE: {test_MAE:.3f}")
        print(f"Depth: {depth:2} \tTrain MSE: {train_MSE:.3f} \tTest MSE: {test_MSE:.3f}")
        print(f"Depth: {depth:2} \tTrain R2: {train_R2:.3f} \tTest R2: {test_R2:.3f}")

except Exception as e:
    print("Error during Random Forest optimization:", e)

try:
    # Train MAE vs. Test MAE
    plt.plot(max_depth_range, train_MAEs, label="Train MAE", marker='o')
    plt.plot(max_depth_range, test_MAEs, label="Test MAE", marker='o')
    plt.xlabel("Tree Depth")
    plt.ylabel("MAE")
    plt.title("Random Forest Regressor: MAE vs. Depth")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Train MSE vs. Test MSE
    plt.plot(max_depth_range, train_MSEs, label="Train MSE", marker='o')
    plt.plot(max_depth_range, test_MSEs, label="Test MSE", marker='o')
    plt.xlabel("Tree Depth")
    plt.ylabel("MSE")
    plt.title("Random Forest Regressor: MSE vs. Depth")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Train R2 vs. Test R2
    plt.plot(max_depth_range, train_R2s, label="Train R2", marker='o')
    plt.plot(max_depth_range, test_R2s, label="Test R2", marker='o')
    plt.xlabel("Tree Depth")
    plt.ylabel("R2")
    plt.title("Random Forest Regressor: R2 vs. Depth")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Bias-Variance Tradeoff
    plt.figure(figsize=(10, 6))
    plt.plot(max_depth_range, train_MAEs, label="Training error (Bias)", marker='o')
    plt.plot(max_depth_range, test_MAEs, label="Test error (Variance)", marker='o')
    plt.axvline(x=max_depth_range[np.argmin(test_MAEs)], color='green', linestyle='--', label="Optimal depth")
    plt.title("Bias-Variance Tradeoff")
    plt.xlabel("Tree Depth")
    plt.ylabel("Mean Squared Error (MSE)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

except Exception as e:
    print("Error during analysis:", e)


# Vorhersage mit dem trainierten Random Forest Modell
try:
    # Predict electricity price for a new sample from test data
    sample = X_test.iloc[0:1]
    prediction = model.predict(sample)
    print("Sample features:\n", sample)
    print("Predicted electricity price:", prediction[0])
    print("Actual electricity price:", y_test.iloc[0])

except Exception as e:
    print("Error during prediction:", e)