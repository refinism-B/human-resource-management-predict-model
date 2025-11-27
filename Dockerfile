# 使用官方 Python 映像檔作為基底
FROM python:3.12-slim

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt（如果有的話）
COPY requirements.txt .

# 安裝依賴套件
RUN pip install --no-cache-dir -r requirements.txt

# 複製你的 Streamlit 程式碼
COPY streamlit.py .

# 開放 Streamlit 預設的埠號 8501
EXPOSE 8501

# 設定啟動指令，啟動 Streamlit 應用
CMD ["streamlit", "run", "streamlit.py", "--server.enableCORS=false", "--server.port=8501", "--server.address=0.0.0.0"]
