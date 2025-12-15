# 直播錄影人力預測系統

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Scikit--learn](https://img.shields.io/badge/Machine%20Learning-Scikit--learn-orange) ![Status](https://img.shields.io/badge/Status-Experimental-yellow)

## 專案簡介 (Introduction)

**直播錄影人力預測系統** 是一個基於機器學習（Random Forest）的輔助決策工具，旨在解決專案管理中人力排程依賴人工經驗、計算繁瑣且易有誤差的問題。

本專案利用 2024-2025 年間的真實專案執行數據，透過特徵工程將非結構化的業務需求轉化為模型特徵，預測各類專案所需的最佳人力配置，協助管理者進行更精準的資源規劃。

### 核心價值 (Business Value)
*   **效率提升**：將繁瑣的人力計算流程自動化，減少行政作業時間。
*   **數據驅動**：將「經驗法則」轉化為「數據模型」，提供客觀的派工依據。
*   **易用性**：結合 GUI 圖形介面，讓非技術背景的行政人員也能輕鬆使用。

---

## 技術架構 (Tech Stack)

*   **語言**：Python
*   **資料處理**：Pandas, NumPy
*   **機器學習**：Scikit-learn (RandomForestRegressor)
*   **圖形介面**：Tkinter、Streamlit

---

## 資料處理與特徵工程 (Data Pipeline)

原始資料來自真實業務場景，需經過嚴謹的清洗與轉換才能用於訓練。

### 1. 資料預處理 (Preprocessing)
*   **資料清洗**：處理缺失值與異常值，確保資料品質。
*   **時間特徵轉換**：
    *   將絕對時間（如 `10:00-14:00`）轉換為相對時長（`4.0 Hours`）。
    *   拆解日期因子（月/日/星期），並針對「是否為假日」進行 **One-Hot Encoding**。
*   **類別特徵編碼**：
    *   針對「專案性質」與「特殊需求」進行 One-Hot Encoding，將業務邏輯數值化。

### 2. 模型訓練 (Model Training)
*   **演算法**：Random Forest Regressor (隨機森林迴歸)
*   **參數設定**：
    *   `n_estimators = 150`
    *   `min_samples_split = 2`
*   **資料集劃分**：80% 訓練集 / 20% 測試集

---

## 模型表現 (Performance)

模型在測試集上的表現如下，考慮到人力配置通常為整數（0-8人），**RMSE 0.507** 代表預測誤差控制在 ±0.5 人以內，具有高度參考價值。

| Metric | Value | Description |
| :--- | :--- | :--- |
| **MSE** | 0.257 | 均方誤差 |
| **RMSE** | **0.507** | 均方根誤差 (主要參考指標) |

---

## 🚀 如何執行 (Usage)

### 1. 安裝依賴 (Installation)
```bash
pip install pandas scikit-learn numpy
# 若有 requirements.txt
# pip install -r requirements.txt
```

### 2. 執行程式 (Run)
```bash
# 啟動 GUI 介面 (請依實際檔名修改)
python main.py
```

---

## 未來展望 (Future Roadmap)

本專案目前為單機實驗性質，未來規劃進行以下優化：

1.  **自動化 ETL 管線**：建立自動化資料清洗流程，提升資料處理效率。
2.  **資料庫整合**：引入 SQL 資料庫取代 CSV 存儲，確保資料一致性與安全性。
3.  **排班最佳化**：結合人員技能標籤，從預測「人數」升級為推薦具體的「人員名單」。
4.  **持續整合 (CI/CT)**：建立模型再訓練機制，隨著新資料累積自動更新模型參數。
