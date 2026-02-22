import re  # 引入正規表達式，處理文字用

def srt_to_text(file_path: str) -> str:
    """
    將 .srt 字幕檔轉成純文字
    """
    # Step 2-2️⃣：讀檔
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Step 2-3️⃣：移除時間碼
    content = re.sub(
        r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}",
        "",
        content
    )

    # Step 2-4️⃣：移除字幕編號
    content = re.sub(r"^\d+$", "", content, flags=re.MULTILINE)

    # Step 2-5️⃣：清理空行並合併成一段文字
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    return " ".join(lines)


