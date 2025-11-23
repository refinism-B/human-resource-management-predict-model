import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import joblib
import pandas as pd

# 載入模型
model_path = r"C:\Users\add41\Documents\Data_Engineer\Project\human-resource-management-predict-model\model\20250612_RFM.pkl"
model = joblib.load(model_path)

# 建立主視窗
root = tk.Tk()
root.title("人力預測系統")
root.geometry("600x600")

# 定義輸入資料框架
input_frame = tk.Frame(root)
input_frame.pack(pady=20)

# 定義輸入欄位和下拉式選單
labels = [
    "幾月？", "幾號？", "星期幾？", "是假日嗎？", "活動多長？",
    "機位數有幾機？", "有花絮嗎？", "有視訊切換或視訊工程嗎？",
    "有視訊連線嗎？", "有負責PA音控嗎？", "會一大場分為多個分場嗎？", "專案性質是？"
]

fields = {}
options = {
    "是假日嗎？": ["是", "不是"],  # 內部轉換為 1/0
    "有花絮嗎？": ["有", "沒有"],  # 內部轉換為 1/0
    "有視訊切換或視訊工程嗎？": ["有", "沒有"],  # 內部轉換為 1/0
    "有視訊連線嗎？": ["有", "沒有"],  # 內部轉換為 1/0
    "有負責PA音控嗎？": ["有", "沒有"],  # 內部轉換為 1/0
    "會一大場分為多個分場嗎？": ["會", "不會"],  # 改為「會/不會」
    "專案性質是？": ["進場", "直播", "錄製"]
}

for label in labels:
    frame = tk.Frame(input_frame)
    frame.pack(fill="x", pady=5)

    tk.Label(frame, text=label, width=20, anchor="w").pack(side="left")

    if label in options:
        combo = ttk.Combobox(frame, values=options[label], state="readonly")
        combo.pack(side="left", fill="x", expand=True)
        fields[label] = combo
    else:
        entry = tk.Entry(frame)
        entry.pack(side="left", fill="x", expand=True)
        fields[label] = entry

# 定義檔案匯入功能


def import_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            importing = pd.read_csv(file_path)
            global new_data
            new_data = importing.drop(columns=['專案', '日期'])
            predict()
        except Exception as e:
            messagebox.showerror("錯誤", f"檔案讀取失敗: {e}")

# 定義預測功能


def predict():
    try:
        # 檢查是否為手動輸入資料
        if 'new_data' not in globals():
            # 收集輸入資料
            data = {
                '月': fields["幾月？"].get(),
                '日': fields["幾號？"].get(),
                '星期': fields["星期幾？"].get(),
                '是否假日': 1 if fields["是假日嗎？"].get() == "是" else 0,
                '時長': fields["活動多長？"].get(),
                '機位數量': fields["機位數有幾機？"].get(),
                '花絮': 1 if fields["有花絮嗎？"].get() == "有" else 0,
                '視訊切換': 1 if fields["有視訊切換或視訊工程嗎？"].get() == "有" else 0,
                '視訊連線': 1 if fields["有視訊連線嗎？"].get() == "有" else 0,
                'PA音控': 1 if fields["有負責PA音控嗎？"].get() == "有" else 0,
                '大場分小場': 1 if fields["會一大場分為多個分場嗎？"].get() == "會" else 0,
                '工作性質_直播': 1 if fields["專案性質是？"].get() == "直播" else 0,
                '工作性質_進場': 1 if fields["專案性質是？"].get() == "進場" else 0,
                '工作性質_錄製': 1 if fields["專案性質是？"].get() == "錄製" else 0,
            }
            global new_data
            new_data = pd.DataFrame([data])

        # 執行模型預測
        pred_data = model.predict(new_data)
        pred_col = ['導播人數', '攝影人數', '音控人數', '直播人數',
                    '機動人數', '花絮人數', '視訊切換人數', '視訊連線人數', '人數']
        output = pd.DataFrame(pred_data, columns=pred_col)

        # 顯示結果
        result_window = tk.Toplevel(root)
        result_window.title("預測結果")
        result_window.geometry("800x400")

        tk.Label(result_window, text="預測結果：", font=("Arial", 14)).pack(pady=10)

        # 創建表格
        tree = ttk.Treeview(result_window, columns=pred_col,
                            show="headings", height=10)
        tree.pack(fill="both", expand=True)

        # 設定表格欄位名稱與寬度
        for col in pred_col:
            tree.heading(col, text=col)  # 設定欄位名稱
            tree.column(col, width=80, anchor="center")  # 設定欄位寬度與對齊方式

        # 插入數據，並格式化為小數點後兩位
        for row in output.values:
            formatted_row = [f"{val:.2f}" for val in row]  # 保留小數點後兩位
            tree.insert("", "end", values=formatted_row)

    except Exception as e:
        messagebox.showerror("錯誤", f"預測失敗: {e}")


# 定義按鈕
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="手動輸入", command=predict).pack(
    side="left", padx=10)
tk.Button(button_frame, text="匯入檔案", command=import_file).pack(
    side="left", padx=10)

# 啟動主迴圈
root.mainloop()
