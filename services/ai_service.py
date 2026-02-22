
from openai import OpenAI
import time
from typing import List

# =====================================================
# 建立 OpenAI Client（只初始化一次）
# =====================================================
client = OpenAI()
MODEL_NAME = "gpt-4.1-mini"

# =====================================================
# Prompt Templates
# =====================================================
YOUTUBE_DESCRIPTION_PROMPT = """
你是一位專業的 YouTube 影片企劃編輯。

請根據以下「字幕內容」，產生一段適合放在 YouTube 的影片說明（Description）：
- 語氣自然、吸引人
- 說清楚影片會學到什麼
- 適合教育 / 教學類頻道
- 使用繁體中文

字幕內容如下：
{text}
"""

HASHTAG_PROMPT = """
你是一位熟悉 YouTube 與社群平台 SEO 的行銷企劃。

請根據以下影片內容，產生 5～8 個適合使用的 Hashtags：
- 使用 # 開頭
- 與 Python、教學、程式學習相關
- 使用繁體中文為主，可搭配英文

影片內容如下：
{text}
"""

PLAN_PROMPT = """
你是一位專業的影音企劃與內容策劃。

請根據以下資料，產出一份「影片企劃書」，格式清楚、可直接交付給 PM 或客戶。

請包含以下段落：
1. 企劃名稱
2. 影片目標
3. 影片內容大綱
4. 影片腳本摘要
5. YouTube 發佈資訊（Description + Hashtags）
6. 建議目標族群

請使用繁體中文，語氣專業但好理解。

【字幕內容】
{text}

【摘要】
{summary}

【影片腳本】
{script}

【YouTube Description】
{description}

【Hashtags】
{hashtags}
"""

# =====================================================
# API 呼叫工具（含重試機制）
# =====================================================
def call_openai_with_retry(prompt: str, retries: int = 3, wait: int = 2) -> str:
    """
    呼叫 OpenAI API，並在失敗時自動重試。

    Parameters
    ----------
    prompt : str
        要送給模型的完整提示詞。
    retries : int
        最大重試次數（預設 3 次）。
    wait : int
        每次重試等待秒數的基礎值（會隨次數遞增）。

    Returns
    -------
    str
        模型回傳文字；若多次失敗則回傳錯誤提示字串。
    """
    for attempt in range(1, retries + 1):
        try:
            response = client.responses.create(
                model=MODEL_NAME,
                input=prompt
            )
            result = response.output_text.strip()
            if result:
                return result
            raise ValueError("Empty response from model")
        except Exception:
            if attempt == retries:
                return "⚠️ AI 產生失敗（已多次嘗試）"
            time.sleep(wait * attempt)

# =====================================================
# 長文本切段工具
# =====================================================
def split_text(text: str, max_chars: int = 1500) -> List[str]:
    """
    將長文字依行切割成多段，避免 token 過長導致 API 失敗。

    Parameters
    ----------
    text : str
        原始字幕文字。
    max_chars : int
        每段最大字元數（預設 1500）。

    Returns
    -------
    List[str]
        切割後的文字段落列表。
    """
    chunks = []
    current_chunk = ""
    for line in text.splitlines():
        if len(current_chunk) + len(line) > max_chars:
            chunks.append(current_chunk)
            current_chunk = line + "\n"
        else:
            current_chunk += line + "\n"
    if current_chunk.strip():
        chunks.append(current_chunk)
    return chunks

# =====================================================
# AI 功能函式
# =====================================================
def summarize_text(text: str) -> str:
    """
    對長字幕進行摘要，支援自動切段。

    Parameters
    ----------
    text : str
        原始字幕內容。

    Returns
    -------
    str
        整合後的影片摘要。
    """
    chunks = split_text(text)
    partial_summaries = []
    for idx, chunk in enumerate(chunks, start=1):
        prompt = f"請將以下第 {idx} 段字幕整理成重點摘要：\n\n{chunk}"
        partial_summaries.append(call_openai_with_retry(prompt))
    final_prompt = f"請將以下多段摘要整合成一段完整影片摘要：\n\n{chr(10).join(partial_summaries)}"
    return call_openai_with_retry(final_prompt)

def script_from_text(text: str) -> str:
    """
    根據字幕產生口語化影片講稿。

    Parameters
    ----------
    text : str
        原始字幕內容。

    Returns
    -------
    str
        影片講稿文字。
    """
    prompt = f"請根據以下字幕內容，產生一份口語化的影片講稿：\n{text}"
    return call_openai_with_retry(prompt)

def youtube_description(text: str) -> str:
    """
    產生 YouTube 影片 Description。

    Parameters
    ----------
    text : str
        原始字幕內容。

    Returns
    -------
    str
        適合發布的 Description。
    """
    prompt = YOUTUBE_DESCRIPTION_PROMPT.format(text=text)
    return call_openai_with_retry(prompt)

def generate_hashtags(text: str) -> str:
    """
    產生 YouTube / 社群平台 Hashtags。

    Parameters
    ----------
    text : str
        原始字幕內容。

    Returns
    -------
    str
        Hashtag 字串。
    """
    prompt = HASHTAG_PROMPT.format(text=text)
    return call_openai_with_retry(prompt)

def translate_text(text: str, target_lang: str) -> str:
    """
    將字幕翻譯為指定語言。

    Parameters
    ----------
    text : str
        原始字幕內容。
    target_lang : str
        目標語言代碼（支援：'en', 'ja'）。

    Returns
    -------
    str
        翻譯後文字。
    """
    lang_map = {"en": "英文", "ja": "日文"}
    if target_lang not in lang_map:
        return "（不支援的語言）"
    prompt = f"請將以下中文字幕翻譯成{lang_map[target_lang]}，保持語意正確、自然流暢：\n\n{text}"
    return call_openai_with_retry(prompt)

def generate_plan(text: str, summary: str, script: str, description: str, hashtags: str) -> str:
    """
    整合所有內容生成完整影片企劃書。

    Parameters
    ----------
    text : str
        原始字幕。
    summary : str
        摘要內容。
    script : str
        影片講稿。
    description : str
        YouTube Description。
    hashtags : str
        Hashtags。

    Returns
    -------
    str
        完整影片企劃書文字。
    """
    prompt = PLAN_PROMPT.format(
        text=text,
        summary=summary,
        script=script,
        description=description,
        hashtags=hashtags
    )
    return call_openai_with_retry(prompt)

