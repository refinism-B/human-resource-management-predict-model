import gradio as gr
import pandas as pd
import joblib
import os
from datetime import datetime

# --- helper functions ---

def find_model_path(filename="20260101_RFM.pkl"):
    """
    Recursively search for the model file in the current directory and subdirectories.
    """
    current_dir = os.getcwd()
    for root, dirs, files in os.walk(current_dir):
        if filename in files:
            return os.path.join(root, filename)
    return None

def load_model(path):
    try:
        if not os.path.exists(path):
            return None, "File not found"
        
        loaded_obj = joblib.load(path)
        
        # Check if the loaded object is a dictionary (new format) or the model itself (old format)
        if isinstance(loaded_obj, dict) and 'model' in loaded_obj:
            model = loaded_obj['model']
            return model, "Model loaded successfully"
        else:
            # Backward compatibility or if the file IS the model
            return loaded_obj, "Model loaded successfully"
            
    except Exception as e:
        return None, str(e)


# --- Global Model Variable ---
# We will try to load it at startup
MODEL_PATH = find_model_path()
MODEL = None
LOAD_STATUS = "Model not loaded"

if MODEL_PATH:
    MODEL, LOAD_STATUS = load_model(MODEL_PATH)

# --- Prediction Logic ---

def predict_single(
    month, day, weekday, 
    is_holiday, duration, camera_count, 
    has_highlights, has_video_switch, has_video_link, 
    has_pa_control, has_multi_venue, project_type
):
    if MODEL is None:
        return "Error: Model not loaded. Please ensure the model file is found.", None

    try:
        # Prepare input data
        # Mapping inputs to model format
        # Note: app.py uses "是"/"不是" or "有"/"沒有" etc. 
        # Here we will ensure inputs from Gradio match or we map them.
        
        # Mappings based on app.py logic
        input_dict = {
            '月': int(month),
            '日': int(day),
            '星期': int(weekday),
            '是否假日': 1 if is_holiday == "是" else 0,
            '時長': float(duration),
            '機位數量': int(camera_count),
            '花絮': 1 if has_highlights == "有" else 0,
            '視訊切換': 1 if has_video_switch == "有" else 0,
            '視訊連線': 1 if has_video_link == "有" else 0,
            'PA音控': 1 if has_pa_control == "有" else 0,
            '大場分小場': 1 if has_multi_venue == "會" else 0,
            '工作性質_直播': 1 if project_type == "直播" else 0,
            '工作性質_進場': 1 if project_type == "進場" else 0,
            '工作性質_錄製': 1 if project_type == "錄製" else 0,
        }
        
        input_df = pd.DataFrame([input_dict])
        
        # Predict
        pred_data = MODEL.predict(input_df)
        pred_col = ['導播人數', '攝影人數', '音控人數', '直播人數',
                    '機動人數', '花絮人數', '視訊切換人數', '視訊連線人數', '人數']
        predictions = pd.DataFrame(pred_data, columns=pred_col)
        
        # Format result
        total_manpower = predictions['人數'].iloc[0]
        
        # Detailed breakdown string
        breakdown_text = f"### 預測總人力: {total_manpower:.1f} 人\n\n"
        breakdown_text += "#### 詳細配置:\n"
        
        position_data = predictions.iloc[0][:-1] # Exclude total
        for pos, val in position_data.items():
            breakdown_text += f"- **{pos}**: {val:.2f}\n"
            
        return breakdown_text, predictions
        
    except Exception as e:
        return f"Prediction Error: {str(e)}", None

def predict_batch(file_obj):
    if MODEL is None:
        return None, "Error: Model not loaded."
    
    if file_obj is None:
        return None, "Error: No file uploaded."
        
    try:
        df = pd.read_csv(file_obj.name)
        
        # Drop columns if they exist (from app.py logic)
        columns_to_drop = ['專案', '日期']
        existing_columns_to_drop = [col for col in columns_to_drop if col in df.columns]
        if existing_columns_to_drop:
            df = df.drop(columns=existing_columns_to_drop)
            
        pred_data = MODEL.predict(df)
        pred_col = ['導播人數', '攝影人數', '音控人數', '直播人數',
                    '機動人數', '花絮人數', '視訊切換人數', '視訊連線人數', '人數']
        predictions = pd.DataFrame(pred_data, columns=pred_col)
        
        temp_filename = f"prediction_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        predictions.to_csv(temp_filename, index=False)
        
        return predictions, temp_filename
        
    except Exception as e:
        return None, f"Batch Prediction Error: {str(e)}"

# --- UI Construction ---


with gr.Blocks(title="直播人力安排預測系統",
                css="div.gradio-container") as demo:
    gr.Markdown("<h1 style='text-align: center; font-size: 2.5em'>直播人力安排預測系統</h1>")
    gr.Markdown("<p style='text-align: center; font-size: 1.2em'>輸入專案參數，系統將預測最佳人力配置。</p>")
    
    with gr.Row():
        status_box = gr.Textbox(value=f"Model Status: {LOAD_STATUS} (Path: {MODEL_PATH})", label="系統狀態", interactive=False)
    
    with gr.Tabs():
        # Tab 1: Manual Input
        with gr.TabItem("手動輸入"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 時間與基本資訊")
                    month = gr.Number(label="幾月？", value=datetime.now().month, minimum=1, maximum=12, step=1)
                    day = gr.Number(label="幾號？", value=datetime.now().day, minimum=1, maximum=31, step=1)
                    weekday = gr.Number(label="星期幾？ (1-7)", value=datetime.now().weekday() + 1, minimum=1, maximum=7, step=1)
                    is_holiday = gr.Dropdown(choices=["是", "不是"], value="不是", label="是假日嗎？")
                    
                with gr.Column():
                    gr.Markdown("### 專案規模")
                    duration = gr.Number(label="活動多長？（小時）", value=3.0, step=0.5)
                    camera_count = gr.Number(label="機位數有幾機？", value=3, step=1)
                    project_type = gr.Dropdown(choices=["進場", "直播", "錄製"], value="直播", label="專案性質")
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 技術需求 A")
                    has_highlights = gr.Dropdown(choices=["有", "沒有"], value="沒有", label="有花絮嗎？")
                    has_video_switch = gr.Dropdown(choices=["有", "沒有"], value="沒有", label="有視訊切換/工程？")
                    has_video_link = gr.Dropdown(choices=["有", "沒有"], value="沒有", label="有視訊連線嗎？")
                    
                with gr.Column():
                    gr.Markdown("### 技術需求 B")
                    has_pa_control = gr.Dropdown(choices=["有", "沒有"], value="沒有", label="有 PA 音控嗎？")
                    has_multi_venue = gr.Dropdown(choices=["會", "不會"], value="不會", label="會分多場嗎？")

            btn_predict = gr.Button("開始預測", variant="primary")
            
            with gr.Row():
                output_text = gr.Markdown(label="預測結果摘要")
            
            with gr.Row():
                output_df = gr.Dataframe(label="詳細數據")

            btn_predict.click(
                predict_single,
                inputs=[
                    month, day, weekday, is_holiday, duration, camera_count,
                    has_highlights, has_video_switch, has_video_link,
                    has_pa_control, has_multi_venue, project_type
                ],
                outputs=[output_text, output_df]
            )

        # Tab 2: Batch Input
        with gr.TabItem("匯入 CSV 檔案"):
            gr.Markdown("上傳包含專案參數的 CSV 檔案進行批次預測。欄位名稱需符合模型要求。")
            file_upload = gr.File(label="上傳 CSV", file_types=[".csv"])
            btn_batch_predict = gr.Button("執行批次預測", variant="primary")
            
            batch_output_df = gr.Dataframe(label="預測結果")
            batch_download = gr.File(label="下載結果 CSV")
            batch_error = gr.Textbox(label="狀態/錯誤訊息", interactive=False)
            
            btn_batch_predict.click(
                predict_batch,
                inputs=[file_upload],
                outputs=[batch_output_df, batch_download] # Note: error msg handling needs wrapper if using simple return, but let's stick to this
            )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
