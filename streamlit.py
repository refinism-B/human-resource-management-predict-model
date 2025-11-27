import streamlit as st
import pandas as pd
import joblib
import os
from datetime import datetime

# 設定頁面配置
st.set_page_config(
    page_title="直播人力安排預測系統",
    page_icon="📹",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 自定義 CSS 樣式
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #0066CC;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border: none;
        margin-top: 1rem;
    }
    .stButton>button:hover {
        background-color: #0052A3;
    }
    div[data-testid="metric-container"] {
        background-color: #f0f2f6;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# 模型路徑配置（請自行填入您的模型路徑）
MODEL_PATH = r"/app/model/20250612_RFM.pkl"

# 初始化 session state
if 'model' not in st.session_state:
    st.session_state.model = None
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False

# 載入模型函式


@st.cache_resource
def load_model(model_path):
    """載入訓練好的模型"""
    try:
        model = joblib.load(model_path)
        return model, True
    except Exception as e:
        return None, False


# 標題和引言
st.title("📹 直播人力安排預測系統")
st.markdown("請輸入專案相關參數，系統將依據歷史數據模型預測最佳人力配置建議。")

# 模型載入狀態檢查
with st.expander("⚙️ 模型設定", expanded=not st.session_state.model_loaded):
    model_path_input = st.text_input(
        "模型檔案路徑 (.pkl)",
        value=MODEL_PATH,
        placeholder="請輸入模型檔案的完整路徑，例如: C:/models/model.pkl"
    )

    if st.button("載入模型"):
        if model_path_input and os.path.exists(model_path_input):
            model, success = load_model(model_path_input)
            if success:
                st.session_state.model = model
                st.session_state.model_loaded = True
                st.success("✅ 模型載入成功！")
            else:
                st.error("❌ 模型載入失敗，請檢查檔案格式是否正確。")
        else:
            st.error("❌ 請輸入有效的模型檔案路徑。")

    if st.session_state.model_loaded:
        st.info(f"✅ 模型已載入：{model_path_input}")

st.divider()

# 輸入方式選擇
input_method = st.radio(
    "選擇輸入方式",
    ["手動輸入", "匯入CSV檔案"],
    horizontal=True
)

if input_method == "手動輸入":
    # 手動輸入區域
    st.subheader("📝 專案參數輸入")

    # 使用容器分組
    with st.container():
        st.markdown("#### 時間與基本資訊")
        col1, col2 = st.columns(2)

        with col1:
            month = st.number_input(
                "幾月？", min_value=1, max_value=12, value=datetime.now().month, step=1)
            day = st.number_input(
                "幾號？", min_value=1, max_value=31, value=datetime.now().day, step=1)
            weekday = st.number_input(
                "星期幾？", min_value=1, max_value=7, value=datetime.now().weekday() + 1, step=1)

        with col2:
            is_holiday = st.selectbox("是假日嗎？", options=["是", "不是"], index=1)
            duration = st.number_input(
                "活動多長？（小時）", min_value=0.5, max_value=24.0, value=3.0, step=0.5)
            camera_count = st.number_input(
                "機位數有幾機？", min_value=1, max_value=20, value=3, step=1)

    with st.container():
        st.markdown("#### 技術需求")
        col3, col4 = st.columns(2)

        with col3:
            has_highlights = st.selectbox(
                "有花絮嗎？", options=["有", "沒有"], index=1)
            has_video_switch = st.selectbox(
                "有視訊切換或視訊工程嗎？", options=["有", "沒有"], index=1)
            has_video_link = st.selectbox(
                "有視訊連線嗎？", options=["有", "沒有"], index=1)

        with col4:
            has_pa_control = st.selectbox(
                "有負責PA音控嗎？", options=["有", "沒有"], index=1)
            has_multi_venue = st.selectbox(
                "會一大場分為多個分場嗎？", options=["會", "不會"], index=1)
            project_type = st.selectbox(
                "專案性質是？", options=["進場", "直播", "錄製"], index=1)

    # 預測按鈕
    st.markdown("---")
    predict_button = st.button(
        "🔮 開始人力預測", type="primary", use_container_width=True)

    if predict_button:
        if not st.session_state.model_loaded:
            st.error("❌ 請先載入模型檔案！")
        else:
            # 準備輸入數據
            input_data = pd.DataFrame([{
                '月': month,
                '日': day,
                '星期': weekday,
                '是否假日': 1 if is_holiday == "是" else 0,
                '時長': duration,
                '機位數量': camera_count,
                '花絮': 1 if has_highlights == "有" else 0,
                '視訊切換': 1 if has_video_switch == "有" else 0,
                '視訊連線': 1 if has_video_link == "有" else 0,
                'PA音控': 1 if has_pa_control == "有" else 0,
                '大場分小場': 1 if has_multi_venue == "會" else 0,
                '工作性質_直播': 1 if project_type == "直播" else 0,
                '工作性質_進場': 1 if project_type == "進場" else 0,
                '工作性質_錄製': 1 if project_type == "錄製" else 0,
            }])

            # 執行預測
            with st.spinner('正在分析人力需求...'):
                try:
                    # 使用真實模型進行預測
                    pred_data = st.session_state.model.predict(input_data)
                    pred_col = ['導播人數', '攝影人數', '音控人數', '直播人數',
                                '機動人數', '花絮人數', '視訊切換人數', '視訊連線人數', '人數']
                    predictions = pd.DataFrame(pred_data, columns=pred_col)

                    # 顯示結果
                    st.success("✅ 預測完成！")
                    st.markdown("---")
                    st.subheader("📊 人力配置預測結果")

                    # 重點指標展示（使用最後一欄 '人數' 作為總人數）
                    total_manpower = predictions['人數'].iloc[0]
                    st.metric(
                        label="預計總人力需求",
                        value=f"{total_manpower:.1f} 人",
                        delta=None,
                        help="根據專案參數預測的總人力需求"
                    )

                    # 詳細結果改為點列式呈現
                    st.markdown("#### 各崗位人力需求明細")

                    # 使用兩欄布局來更好地展示點列
                    col1, col2 = st.columns(2)

                    # 獲取所有崗位數據（排除最後一欄 '人數'）
                    position_data = predictions.iloc[0][:-1]
                    positions = list(position_data.index)

                    # 分成兩組顯示
                    mid_point = len(positions) // 2

                    with col1:
                        for i in range(mid_point):
                            pos = positions[i]
                            value = position_data[pos]
                            st.markdown(f"• **{pos}**: {value:.2f} 人")

                    with col2:
                        for i in range(mid_point, len(positions)):
                            pos = positions[i]
                            value = position_data[pos]
                            st.markdown(f"• **{pos}**: {value:.2f} 人")

                    # 額外的視覺化
                    with st.expander("查看人力分配圖表"):
                        # 準備圖表數據（排除總人數）
                        # 排除最後一欄 '人數'
                        chart_data = predictions.iloc[0][:-1].to_dict()
                        chart_df = pd.DataFrame(
                            list(chart_data.items()), columns=['崗位', '人數'])
                        chart_df = chart_df.sort_values('人數', ascending=True)

                        # 使用 Streamlit 的原生圖表
                        st.bar_chart(chart_df.set_index('崗位'))

                except Exception as e:
                    st.error(f"❌ 預測失敗：{str(e)}")

else:  # CSV檔案匯入
    st.subheader("📁 CSV檔案匯入")

    uploaded_file = st.file_uploader(
        "選擇CSV檔案",
        type=['csv'],
        help="請上傳包含專案參數的CSV檔案"
    )

    if uploaded_file is not None:
        try:
            # 讀取CSV檔案
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ 成功讀取檔案：{uploaded_file.name}")

            # 顯示原始數據預覽
            with st.expander("查看原始數據"):
                st.dataframe(df.head())

            # 檢查並移除不需要的欄位
            columns_to_drop = ['專案', '日期']
            existing_columns_to_drop = [
                col for col in columns_to_drop if col in df.columns]
            if existing_columns_to_drop:
                df = df.drop(columns=existing_columns_to_drop)
                st.info(f"已移除欄位：{', '.join(existing_columns_to_drop)}")

            # 批次預測按鈕
            if st.button("🔮 執行批次預測", type="primary", use_container_width=True):
                if not st.session_state.model_loaded:
                    st.error("❌ 請先載入模型檔案！")
                else:
                    with st.spinner(f'正在預測 {len(df)} 筆資料...'):
                        try:
                            # 使用模型進行批次預測
                            pred_data = st.session_state.model.predict(df)
                            pred_col = ['導播人數', '攝影人數', '音控人數', '直播人數',
                                        '機動人數', '花絮人數', '視訊切換人數', '視訊連線人數', '人數']
                            predictions = pd.DataFrame(
                                pred_data, columns=pred_col)

                            # 顯示結果
                            st.success(f"✅ 成功預測 {len(predictions)} 筆資料！")
                            st.markdown("---")
                            st.subheader("📊 批次預測結果")

                            # 統計資訊
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("預測筆數", f"{len(predictions)} 筆")
                            with col2:
                                avg_total = predictions['人數'].mean()
                                st.metric("平均總人力", f"{avg_total:.1f} 人")
                            with col3:
                                max_total = predictions['人數'].max()
                                st.metric("最大人力需求", f"{max_total:.1f} 人")

                            # 詳細結果表格
                            st.markdown("#### 預測結果明細")
                            st.dataframe(
                                predictions,
                                use_container_width=True,
                                height=400,
                                column_config={
                                    col: st.column_config.NumberColumn(
                                        col,
                                        format="%.2f",
                                        width="small"
                                    ) for col in pred_col
                                }
                            )

                            # 下載結果
                            csv = predictions.to_csv(index=False)
                            st.download_button(
                                label="📥 下載預測結果",
                                data=csv,
                                file_name=f"prediction_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv"
                            )

                        except Exception as e:
                            st.error(f"❌ 批次預測失敗：{str(e)}")

        except Exception as e:
            st.error(f"❌ 檔案讀取失敗：{str(e)}")

# 頁尾資訊
st.markdown("---")
st.caption("💡 提示：此系統基於歷史數據模型進行預測，實際人力需求可能因現場情況有所調整。")
