from mod import train_mod as tm
import pandas as pd
from sklearn.model_selection import GridSearchCV, train_test_split

data = tm.read_data()

data = data.drop(columns=['編號', '專案', '日期'])

data = pd.get_dummies(data, columns=['工作性質'])

X, y = tm.separate_features_labels(data=data)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

print("開始訓練並尋找最佳模型...")
best_model = tm.train_and_get_best_model(X_train=X_train, y_train=y_train)

mse, rmse, r2 = tm.validation_model(
    best_model=best_model, X_test=X_test, y_test=y_test)

print(f"均方誤差 (MSE): {mse:.4f}")
print(f"均方根誤差 (RMSE): {rmse:.4f}")
print(f"R-squared 分數: {r2:.4f}")

tm.save_model(model=best_model, feature_data=X)
print("模型儲存完畢！")
