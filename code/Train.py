"""
Train.py
--------
This script handles the training pipeline for the Human Resource Management Prediction Model.
It reads data, processes features, trains a Random Forest model, and evaluates its performance.
"""

from mod import train_mod as tm
import pandas as pd
from sklearn.model_selection import train_test_split

def main():
    print("=== Model Training Pipeline Started ===")

    # 1. Load Data
    print("[1/5] Reading data...")
    try:
        data = tm.read_data()
    except Exception as e:
        print(f"Error reading data: {e}")
        return

    # 2. Preprocess Data
    print("[2/5] Preprocessing data...")
    # Drop irrelevant columns for training
    if '編號' in data.columns:
        data = data.drop(columns=['編號'])
    if '專案' in data.columns:
        data = data.drop(columns=['專案'])
    if '日期' in data.columns:
        data = data.drop(columns=['日期'])
        
    # One-Hot Encoding for categorical variables
    data = pd.get_dummies(data, columns=['工作性質'])

    # Separate features (X) and labels (y)
    X, y = tm.separate_features_labels(data=data)
    
    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 3. Train Model
    print("[3/5] Training model (GridSearchCV)...")
    best_model = tm.train_and_get_best_model(X_train=X_train, y_train=y_train)

    # 4. Evaluate Model
    print("[4/5] Evaluating model performance...")
    mse, rmse, r2 = tm.validation_model(
        best_model=best_model, X_test=X_test, y_test=y_test
    )

    print("-" * 30)
    print(f"Mean Squared Error (MSE): {mse:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
    print(f"R-squared (R2): {r2:.4f}")
    print("-" * 30)

    # 5. Save Model
    print("[5/5] Saving model...")
    tm.save_model(model=best_model, feature_data=X)
    print("Model saved successfully!")
    print("=== Pipeline Completed ===")

if __name__ == "__main__":
    main()

