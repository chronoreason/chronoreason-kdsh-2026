def chunk_text(text, chunk_size=800, overlap=100):
    """Split text into overlapping chunks of words.
    
    Args:
        text: Input text to chunk
        chunk_size: Number of words per chunk (default 800)
        overlap: Number of overlapping words between chunks (default 100)
    
    Returns:
        List of text chunks
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if not text or not text.strip():
        return []
    
    words = text.split()
    if not words:
        return []

    # Prevent negative or zero step size when overlap exceeds chunk_size.
    effective_overlap = max(0, min(overlap, chunk_size - 1))
    step = max(1, chunk_size - effective_overlap)
    
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += step
        if start >= len(words):
            break

    return chunks
