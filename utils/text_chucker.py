def split_text(text: str, max_chars: int = 1500) -> list[str]:
    chunks = []
    current = ""

    for line in text.splitlines():
        if len(current) + len(line) > max_chars:
            chunks.append(current)
            current = line + "\n"
        else:
            current += line + "\n"

    if current.strip():
        chunks.append(current)

    return chunks
