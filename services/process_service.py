if not file_path.endswith((".srt", ".txt")):
    raise ValueError("不支援的檔案格式")

from utils.subtitle_parser import srt_to_text
from services.ai_service import (
    summarize_text,
    script_from_text,
    youtube_description,
    generate_hashtags
)

def process_subtitle(srt_path: str) -> dict:
    text = srt_to_text(srt_path)

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
