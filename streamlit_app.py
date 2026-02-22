import streamlit as st
import tempfile
import os
def process_subtitle(file_path: str) -> dict:
    """
    上傳 → 解析 → AI → 輸出
    """
    text = srt_to_text(file_path)

    summary = summarize_text(text)
    script = script_from_text(text)
    description = youtube_description(text)
    hashtags = generate_hashtags(text)

    return {
        "text": text,
        "summary": summary,
        "script": script,
        "description": description,
        "hashtags": hashtags
    }

from utils.subtitle_parser import srt_to_text
from services.ai_service import (
    summarize_text,
    script_from_text,
    youtube_description,
    generate_hashtags
)

st.set_page_config(
    page_title="Video AI Tool",
    layout="wide"
)

st.title("🎬 Video AI Tool")
st.write("上傳字幕檔，自動產生影片內容")

uploaded_file = st.file_uploader(
    "請上傳字幕檔 (.srt 或 .txt)",
    type=["srt", "txt"]
)

if uploaded_file and st.button("🚀 產生內容"):
    try:
        with st.spinner("AI 處理中，請稍候..."):

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=os.path.splitext(uploaded_file.name)[1]
            ) as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name

            result = process_subtitle(tmp_path)

            st.subheader("📄 字幕純文字")
            st.text_area("", result["text"], height=150)

            st.subheader("🧠 AI 摘要")
            st.write(result["summary"])

            st.subheader("🎥 影片腳本初稿")
            st.write(result["script"])

            st.subheader("📺 YouTube Description")
            st.write(result["description"])

            st.subheader("#️⃣ Hashtags")
            st.write(result["hashtags"])

    except Exception as e:
        st.error("❌ 處理過程發生錯誤，請確認檔案格式或稍後再試")
        st.exception(e) 
