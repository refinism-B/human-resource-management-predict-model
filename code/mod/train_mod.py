import os

import joblib
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.multioutput import MultiOutputRegressor
from mod.config import LABELS, FEATURES, PARAM_GRID


load_dotenv()
path = os.environ.get("data_path")
save_path = os.environ.get("model_path")


def read_data(path=path):
    data = pd.read_csv(path)

    return data


def separate_features_labels(data, features=FEATURES, labels=LABELS):
    X = data[features]
    y = data[labels]

    return X, y


def train_and_get_best_model(X_train, y_train, param_grid=PARAM_GRID):
    rf = RandomForestRegressor(random_state=42)
    multi_rf = MultiOutputRegressor(rf)
    grid_search = GridSearchCV(multi_rf, param_grid=param_grid,
                               cv=5, scoring='neg_mean_squared_error', n_jobs=-1, verbose=3)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_

    return best_model


def validation_model(best_model, X_test, y_test):
    y_pred = best_model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    return mse, rmse, r2


def save_model(model, feature_data, save_path=save_path):
    model_data = {
        'model': model,
        'features': feature_data.columns.tolist()
    }

    joblib.dump(model_data, save_path, compress=3)
