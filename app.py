import streamlit as st
import os
import json
from utils.subtitle_parser import srt_to_text
from services.ai_service import (
    summarize_text,
    script_from_text,
    youtube_description,
    generate_hashtags,
    translate_text,
    generate_plan
)
from utils.file_writer import (
    save_uploaded_file,
    generate_output_filename,
    save_output_file
)

# ========= 資料夾初始化 =========
INPUT_DIR = "data/input"
OUTPUT_DIR = "data/output"
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ========= UI 設定 =========
st.set_page_config(page_title="🎬 Video AI Tool")
st.title("🎬 Video AI Tool")
st.write("一次上傳多個字幕檔，自動產生影片內容、多語系翻譯與企劃書")

uploaded_files = st.file_uploader(
    "請上傳字幕檔（可多選 .srt / .txt）",
    type=["srt", "txt"],
    accept_multiple_files=True
)

if not uploaded_files:
    st.info("請至少上傳一個字幕檔")
    st.stop()

# ========= 主流程 =========
if st.button("🚀 批次產生 AI 內容"):

    st.success(f"共收到 {len(uploaded_files)} 個檔案，開始處理...")
    progress_bar = st.progress(0)

    for index, uploaded_file in enumerate(uploaded_files, start=1):

        st.write(f"### 📄 處理檔案：{uploaded_file.name}")

        # ========= 1️⃣ 儲存到 data/input =========
        input_file_path = save_uploaded_file(uploaded_file)

        # ========= 2️⃣ 解析字幕 =========
        subtitle_text = srt_to_text(input_file_path)

        if len(subtitle_text.strip()) < 50:
            st.warning("⚠️ 字幕內容太短，已跳過")
            continue

        # ========= 3️⃣ AI 生成 =========
        with st.spinner("🤖 AI 生成中..."):

            summary_text = summarize_text(subtitle_text)
            script_text = script_from_text(subtitle_text)
            description_text = youtube_description(subtitle_text)
            hashtags_text = generate_hashtags(subtitle_text)

            translation_en = translate_text(subtitle_text, "en")
            translation_ja = translate_text(subtitle_text, "ja")

            plan_content = generate_plan(
                subtitle_text,
                summary_text,
                script_text,
                description_text,
                hashtags_text
            )

        st.write(f"🧪 企劃書字數：{len(plan_content)}")

        # ========= 4️⃣ 儲存所有結果到 JSON =========
        result_data = {
            "original_file": uploaded_file.name,
            "zh": subtitle_text,
            "en": translation_en,
            "ja": translation_ja,
            "summary": summary_text,
            "script": script_text,
            "description": description_text,
            "hashtags": hashtags_text,
            "plan": plan_content
        }

        json_path = generate_output_filename(uploaded_file.name, "all")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result_data, f, ensure_ascii=False, indent=4)

        st.write(f"✅ JSON 已儲存：{os.path.basename(json_path)}")

        progress_bar.progress(index / len(uploaded_files))

    st.balloons()
    st.success("🎉 所有檔案處理完成！請查看 data/output/")









