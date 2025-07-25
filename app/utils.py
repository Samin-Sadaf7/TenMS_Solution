import re

def bm25_tokenizer(text: str):
    # Clean and tokenize text (simple word tokenizer)
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text.split()
