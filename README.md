---
title: Human Resource Prediction
emoji: 🎥
colorFrom: blue
colorTo: green
sdk: gradio
app_file: app.py
pinned: false
---
# Live Streaming Manpower Prediction System

![Python](https://img.shields.io/badge/Python-3.11%2B-blue) ![Scikit--learn](https://img.shields.io/badge/Machine%20Learning-Scikit--learn-orange) ![Gradio](https://img.shields.io/badge/GUI-Gradio-red) ![Status](https://img.shields.io/badge/Status-Experimental-yellow)

## Introduction

The **Live Streaming Manpower Prediction System** is a decision support tool based on Machine Learning (Random Forest). It is designed to address the challenges in project management where manpower scheduling often relies on subjective experience, involves tedious calculations, and is prone to errors.

Leveraging real-world project execution data from 2024-2025, this project transforms unstructured business requirements into model features through feature engineering. It predicts the optimal manpower allocation for various project types, enabling managers to perform more precise resource planning.

### Business Value
*   **Efficiency**: Automates the tedious manpower calculation process, reducing administrative time.
*   **Data-Driven**: Transforms "rules of thumb" into "data models," providing an objective basis for dispatching.
*   **Usability**: Offers both **Tkinter** (Desktop) and **Gradio** (Web) interfaces, making it accessible to non-technical administrative staff.

---

## Tech Stack

*   **Language**: Python
*   **Data Processing**: Pandas, NumPy
*   **Machine Learning**: Scikit-learn (RandomForestRegressor)
*   **GUI**: Tkinter, Gradio

---

## Interface Preview

This project provides two interfaces tailored to different usage scenarios:

### 1. Gradio Web App (Modern Web Interface)
Ideal for browser-based operations with a sleek and intuitive design.
![Gradio Demo](https://i.meee.com.tw/aylepi6.png)

### 2. Tkinter GUI (Native Desktop Interface)
Suitable for lightweight local environments without the need for a browser.
![Tkinter Demo](https://i.meee.com.tw/dXyLU37.png)

---

## Data Pipeline & Feature Engineering

The raw data is derived from actual business scenarios and undergoes rigorous cleaning and transformation before training.

### 1. Preprocessing
*   **Data Cleaning**: Handling missing values and outliers to ensure data quality.
*   **Time Feature Transformation**:
    *   Converts absolute time (e.g., `10:00-14:00`) into relative duration (e.g., `4.0 Hours`).
    *   Decomposes date factors (Month/Day/Weekday) and applies **One-Hot Encoding** for "Is Holiday".
*   **Categorical Feature Encoding**:
    *   Applies One-Hot Encoding to "Project Type" and "Technical Requirements" to digitize business logic.

### 2. Model Training
*   **Algorithm**: Random Forest Regressor
*   **Parameters**:
    *   `n_estimators = 150`
    *   `min_samples_split = 2`
*   **Dataset Split**: 80% Training / 20% Testing

---

## Performance

The model's performance on the test set is as follows. Considering that manpower allocation is typically an integer (0-8 people), an **RMSE of 0.507** indicates that the prediction error is controlled within ±0.5 people, making it highly reliable.

| Metric | Value | Description |
| :--- | :--- | :--- |
| **MSE** | 0.257 | Mean Squared Error |
| **RMSE** | **0.507** | Root Mean Squared Error (Primary Metric) |

---

## Usage

Choose the execution method that best fits your workflow.

### 0. Prerequisites
Before the first run, ensure your Python environment is set up and install the required packages:
```bash
pip install -r ./deploy/requirements.txt
```

### 1-1. Tkinter GUI (Desktop App)
Best for users who prefer traditional windowed applications.
1.  Locate the `tkinter.bat` file in the project directory.
2.  **Double-click** to launch the application window.

### 1-2. Gradio Web App (Web Interface)
Best for users who prefer a modern browser interface.
1.  Locate the `gradio.bat` file in the project directory.
2.  **Double-click** to execute the startup script.
3.  **Open your browser** and navigate to `http://127.0.0.1:7860` to access the interface.

---

## Future Roadmap

This project is currently an experimental standalone version. Future optimization plans include:

1.  **Automated ETL Pipeline**: Establish an automated data cleaning process to improve efficiency.
2.  **Database Integration**: Introduce SQL databases to replace CSV storage, ensuring data consistency and security.
3.  **Scheduling Optimization**: Integrate staff skill tags to upgrade from predicting "headcount" to recommending specific "personnel lists."
4.  **CI/CT**: Implement a mechanism for model retraining to automatically update model parameters as new data accumulates.
