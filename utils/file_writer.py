"""
File Manager
負責處理檔案儲存與命名邏輯
"""

import os
from datetime import datetime

# =====================================================
# 資料夾路徑
# =====================================================
INPUT_DIR = "data/input"
OUTPUT_DIR = "data/output"

# 確保資料夾存在
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# =====================================================
# 檔案處理函式
# =====================================================

def save_uploaded_file(uploaded_file) -> str:
    """
    儲存使用者上傳的檔案到 input 資料夾。
    """
    filename = uploaded_file.name
    save_path = os.path.join(INPUT_DIR, filename)

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return save_path


def generate_output_filename(original_name: str, suffix: str, ext: str = "json") -> str:
    """
    產生唯一 output 檔名（避免覆蓋）。

    Parameters
    ----------
    original_name : str
        原始檔名
    suffix : str
        類型標記（例如 summary / plan / script）
    ext : str
        副檔名（預設 json）

    Returns
    -------
    str
        完整輸出路徑
    """
    name_without_ext = os.path.splitext(original_name)[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{name_without_ext}_{suffix}_{timestamp}.{ext}"
    return os.path.join(OUTPUT_DIR, filename)


def save_output_file(content: str, output_path: str):
    """
    將文字內容寫入檔案。
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

