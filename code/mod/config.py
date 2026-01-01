LABELS = ['導播人數', '攝影人數', '音控人數', '直播人數',
          '機動人數', '花絮人數', '視訊切換人數', '視訊連線人數', '人數']

FEATURES = ['月', '日', '星期', '是否假日', '時長', '機位數量', '花絮', '視訊切換',
            '視訊連線', 'PA音控', '大場分小場', '工作性質_直播', '工作性質_進場', '工作性質_錄製']

PARAM_GRID = {
    "estimator__n_estimators": [100, 130, 150, 170, 200, 230, 250, 270, 300],
    "estimator__max_depth": [None, 3, 5, 7, 9, 11, 13],
    "estimator__min_samples_split": [3, 5, 7, 9, 11, 13],
    "estimator__max_features": ['sqrt', 'log2']
}
