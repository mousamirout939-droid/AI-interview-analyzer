"""
lemmatization.py
==================
Lemmatizes tokens to their dictionary base form using NLTK's WordNet
lemmatizer. Falls back to returning the original token if WordNet data
isn't available locally.
"""


def _lemmatizer():
    try:
        from nltk.stem import WordNetLemmatizer
        lemmatizer = WordNetLemmatizer()
        lemmatizer.lemmatize("test")  # trigger data check
        return lemmatizer
    except Exception:
        return None


def lemmatize_word(word: str, pos: str = "n") -> str:
    lemmatizer = _lemmatizer()
    if lemmatizer is None:
        return word.lower()
    try:
        return lemmatizer.lemmatize(word.lower(), pos=pos)
    except Exception:
        return word.lower()


def lemmatize_tokens(tokens: list) -> list:
    lemmatizer = _lemmatizer()
    if lemmatizer is None:
        return [t.lower() for t in tokens]
    return [lemmatizer.lemmatize(t.lower()) for t in tokens]
