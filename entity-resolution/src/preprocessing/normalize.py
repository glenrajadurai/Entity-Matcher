import re
import unicodedata
import pandas as pd
from typing import Optional, Dict

# Standard Country Code Mapping (Supports US, IN, FR, DE, JP, GB, CA, AU + fallback)
COUNTRY_MAP: Dict[str, str] = {
    'UNITED STATES': 'US',
    'UNITED STATES OF AMERICA': 'US',
    'USA': 'US',
    'US': 'US',
    'INDIA': 'IN',
    'IND': 'IN',
    'IN': 'IN',
    'FRANCE': 'FR',
    'FRA': 'FR',
    'FR': 'FR',
    'GERMANY': 'DE',
    'DEUTSCHLAND': 'DE',
    'DEU': 'DE',
    'DE': 'DE',
    'JAPAN': 'JP',
    'JPN': 'JP',
    'JP': 'JP',
    'UNITED KINGDOM': 'GB',
    'GREAT BRITAIN': 'GB',
    'UK': 'GB',
    'GBR': 'GB',
    'GB': 'GB',
    'CANADA': 'CA',
    'CAN': 'CA',
    'CA': 'CA',
    'AUSTRALIA': 'AU',
    'AUS': 'AU',
    'AU': 'AU',
    'BRAZIL': 'BR',
    'BRA': 'BR',
    'BR': 'BR',
    'MEXICO': 'MX',
    'MEX': 'MX',
    'MX': 'MX',
    'ITALY': 'IT',
    'ITA': 'IT',
    'IT': 'IT',
    'SPAIN': 'ES',
    'ESP': 'ES',
    'ES': 'ES',
    'CHINA': 'CN',
    'CHN': 'CN',
    'CN': 'CN'
}

# Business Name Legal Suffix Replacement Mapping
LEGAL_SUFFIX_REPLACEMENTS = [
    (r'\bcorporation\b\.?', 'corp'),
    (r'\bcorp\b\.?', 'corp'),
    (r'\bincorporated\b\.?', 'inc'),
    (r'\binc\b\.?', 'inc'),
    (r'\blimited\b\.?', 'ltd'),
    (r'\bltd\b\.?', 'ltd'),
    (r'\bcompany\b\.?', 'co'),
    (r'\bco\b\.?', 'co'),
    (r'\bgmbh\b\.?', 'gmbh'),
    (r'\bsociete anonyme\b\.?', 'sa'),
    (r'\bs\.?\s*a\.?\b', 'sa'),
    (r'\bsociete a responsabilite limitee\b\.?', 'sarl'),
    (r'\bs\.?\s*a\.?\s*r\.?\s*l\.?\b', 'sarl'),
    (r'\bsas\b\.?', 'sas'),
    (r'\bprivate\b\.?', 'pvt'),
    (r'\bpvt\b\.?', 'pvt'),
    (r'\btechnologies\b\.?', 'tech'),
    (r'\bsolutions\b\.?', 'soln'),
    (r'\benterprises\b\.?', 'ent'),
    (r'\bindustries\b\.?', 'ind')
]

# Address Abbreviation Replacement Mapping
ADDRESS_REPLACEMENTS = [
    (r'\bstreet\b\.?', 'st'),
    (r'\bst\b\.?', 'st'),
    (r'\broad\b\.?', 'rd'),
    (r'\brd\b\.?', 'rd'),
    (r'\bavenue\b\.?', 'ave'),
    (r'\bave\b\.?', 'ave'),
    (r'\bboulevard\b\.?', 'blvd'),
    (r'\bblvd\b\.?', 'blvd'),
    (r'\bapartment\b\.?', 'apt'),
    (r'\bapt\b\.?', 'apt'),
    (r'\bsuite\b\.?', 'ste'),
    (r'\bste\b\.?', 'ste'),
    (r'\bdrive\b\.?', 'dr'),
    (r'\bdr\b\.?', 'dr'),
    (r'\blane\b\.?', 'ln'),
    (r'\bln\b\.?', 'ln'),
    (r'\bcourt\b\.?', 'ct'),
    (r'\bct\b\.?', 'ct'),
    (r'\bplace\b\.?', 'pl'),
    (r'\bpl\b\.?', 'pl'),
    (r'\bhighway\b\.?', 'hwy'),
    (r'\bhwy\b\.?', 'hwy'),
    (r'\bbuilding\b\.?', 'bldg'),
    (r'\bbldg\b\.?', 'bldg')
]


def normalize_unicode(text: str) -> str:
    """
    Normalizes unicode text using NFKD decomposition and removes diacritics / accents.
    Also handles special char replacements like German eszett 'ß' -> 'ss'.
    """
    if not text:
        return ""
    # Handle German eszett before decomposition
    text = text.replace('ß', 'ss').replace('ẞ', 'ss')
    nfkd_form = unicodedata.normalize('NFKD', text)
    # Filter out combining diacritical marks
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def normalize_text(text: str) -> str:
    """
    General text cleaning:
    1. Unicode normalization (stripping diacritics)
    2. Lowercasing
    3. Punctuation normalization
    4. Trimming & collapsing whitespace
    """
    if not isinstance(text, str) or not text.strip():
        return ""
    
    # 1. Unicode normalization
    text = normalize_unicode(text)
    
    # 2. Lowercase
    text = text.lower()
    
    # 3. Punctuation normalization: replace non-alphanumeric (except space/hyphen) with space
    text = re.sub(r'[^\w\s-]', ' ', text)
    
    # 4. Collapse repeated whitespace and trim
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def normalize_business_name(name: Optional[str]) -> Optional[str]:
    """
    Normalizes business names:
    - Lowercase, whitespace, unicode normalization
    - Standardizes legal suffixes (corp, ltd, inc, gmbh, sa, etc.)
    - Preserves core identifying tokens
    """
    if pd.isna(name) or name is None:
        return None
    
    text = normalize_text(str(name))
    if not text:
        return None
    
    # Apply legal suffix rules at word boundaries
    for pattern, replacement in LEGAL_SUFFIX_REPLACEMENTS:
        text = re.sub(pattern, replacement, text)
        
    text = re.sub(r'\s+', ' ', text).strip()
    return text if text else None


def normalize_business_address(address: Optional[str]) -> Optional[str]:
    """
    Normalizes business addresses:
    - Lowercase, whitespace, unicode normalization
    - Standardizes address abbreviations (st, rd, ave, blvd, ste, etc.)
    - Preserves missing address state as None
    """
    if pd.isna(address) or address is None:
        return None
    
    text = normalize_text(str(address))
    if not text:
        return None
    
    # Apply address abbreviation rules at word boundaries
    for pattern, replacement in ADDRESS_REPLACEMENTS:
        text = re.sub(pattern, replacement, text)
        
    text = re.sub(r'\s+', ' ', text).strip()
    return text if text else None


def normalize_country(country: Optional[str]) -> Optional[str]:
    """
    Normalizes country representations:
    - Converts full names/aliases to ISO alpha-2 codes (US, IN, FR, DE, JP, etc.)
    - Supports arbitrary/unseen countries gracefully by cleaning and uppercasing.
    """
    if pd.isna(country) or country is None:
        return None
    
    cleaned = str(country).strip().upper()
    if not cleaned:
        return None
    
    # Lookup in standard mapping
    if cleaned in COUNTRY_MAP:
        return COUNTRY_MAP[cleaned]
    
    # Generic fallback: if 2-letter code, return as is
    if len(cleaned) == 2 and cleaned.isalpha():
        return cleaned
    
    # Return cleaned uppercase fallback for unseen countries
    return cleaned


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies normalization pipeline to an entity dataframe:
    - Preserves exact canonical columns: entity_id, business_name, business_address, country
    - Adds normalized columns: business_name_normalized, business_address_normalized, country_normalized
    - Retains exact row order and entity_id values
    """
    df_out = df.copy()
    
    df_out['business_name_normalized'] = df_out['business_name'].apply(normalize_business_name)
    df_out['business_address_normalized'] = df_out['business_address'].apply(normalize_business_address)
    df_out['country_normalized'] = df_out['country'].apply(normalize_country)
    
    return df_out
