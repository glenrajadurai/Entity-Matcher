import re
from typing import Dict, List, Any, Callable


def soundex(text: str) -> str:
    """
    Computes standard Soundex code for a given string.
    Useful for phonetic blocking of names.
    """
    if not isinstance(text, str) or not text.strip():
        return "Z000"

    clean_text = re.sub(r"[^A-Z]", "", text.upper())
    if not clean_text:
        return "Z000"

    first_letter = clean_text[0]
    mapping = {
        'B': '1', 'F': '1', 'P': '1', 'V': '1',
        'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
        'D': '3', 'T': '3',
        'L': '4',
        'M': '5', 'N': '5',
        'R': '6'
    }

    codes = [mapping.get(ch, '') for ch in clean_text[1:]]

    # Remove consecutive duplicate codes
    compact_codes = []
    prev = None
    for c in codes:
        if c != prev:
            compact_codes.append(c)
            prev = c

    # Remove empty strings (vowels/ignored chars)
    filtered = [c for c in compact_codes if c != '']
    code_str = first_letter + "".join(filtered)
    
    # Pad or truncate to 4 characters
    return (code_str + "0000")[:4]


class BaseBlocker:
    """Base class for blocking key generators."""

    def __init__(self, name: str):
        self.name = name

    def get_key(self, record: Dict[str, Any]) -> str:
        raise NotImplementedError


class ExactBlocker(BaseBlocker):
    """Blocks on exact match of a specific field."""

    def __init__(self, field: str):
        super().__init__(f"ExactBlocker({field})")
        self.field = field

    def get_key(self, record: Dict[str, Any]) -> str:
        val = record.get(self.field, "")
        if val is None or pd_is_nan(val):
            return ""
        return str(val).strip().lower()


class PrefixBlocker(BaseBlocker):
    """Blocks on the first N characters of a text field."""

    def __init__(self, field: str, n_chars: int = 3):
        super().__init__(f"PrefixBlocker({field}, n={n_chars})")
        self.field = field
        self.n_chars = n_chars

    def get_key(self, record: Dict[str, Any]) -> str:
        val = record.get(self.field, "")
        if val is None or pd_is_nan(val):
            return ""
        clean_val = str(val).strip().lower()
        return clean_val[:self.n_chars]


class SoundexBlocker(BaseBlocker):
    """Blocks on the Soundex code of a name field."""

    def __init__(self, field: str):
        super().__init__(f"SoundexBlocker({field})")
        self.field = field

    def get_key(self, record: Dict[str, Any]) -> str:
        val = record.get(self.field, "")
        if val is None or pd_is_nan(val):
            return "Z000"
        return soundex(str(val))


class YearBlocker(BaseBlocker):
    """Extracts year from a date string (e.g. YYYY-MM-DD)."""

    def __init__(self, date_field: str):
        super().__init__(f"YearBlocker({date_field})")
        self.date_field = date_field

    def get_key(self, record: Dict[str, Any]) -> str:
        val = record.get(self.date_field, "")
        if val is None or pd_is_nan(val):
            return ""
        val_str = str(val).strip()
        match = re.search(r"\b(19\d\d|20\d\d)\b", val_str)
        return match.group(1) if match else ""


class CompoundBlocker(BaseBlocker):
    """Combines multiple blocker outputs into a single blocking key."""

    def __init__(self, blockers: List[BaseBlocker]):
        name = "CompoundBlocker(" + ", ".join(b.name for b in blockers) + ")"
        super().__init__(name)
        self.blockers = blockers

    def get_key(self, record: Dict[str, Any]) -> str:
        sub_keys = [b.get_key(record) for b in self.blockers]
        if any(k == "" for k in sub_keys):
            return ""  # If any field is missing, block key is invalid
        return "_".join(sub_keys)


def pd_is_nan(val: Any) -> bool:
    """Helper to safely check if a value is null/NaN."""
    if val is None:
        return True
    try:
        import math
        if isinstance(val, float) and math.isnan(val):
            return True
    except Exception:
        pass
    return False
