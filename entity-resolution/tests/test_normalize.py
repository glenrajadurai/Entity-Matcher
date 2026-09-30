import pytest
import pandas as pd
import numpy as np
from src.preprocessing.normalize import (
    normalize_unicode,
    normalize_text,
    normalize_business_name,
    normalize_business_address,
    normalize_country,
    process_dataframe
)

def test_lowercase_conversion():
    assert normalize_text("ACME LOGISTICS") == "acme logistics"
    assert normalize_business_name("TATA CONSULTANCY SERVICES") == "tata consultancy services"

def test_whitespace_normalization():
    assert normalize_text("  Apex   Solutions   ") == "apex solutions"
    assert normalize_business_address("123   Main   Street,  Suite   400  ") == "123 main st ste 400"

def test_punctuation_normalization():
    assert normalize_text("Acme, Inc. & Co.!") == "acme inc co"
    assert normalize_business_name("Starlight-Tech (Global), Ltd.") == "starlight-tech global ltd"

def test_legal_suffix_normalization():
    assert normalize_business_name("Acme Corporation") == "acme corp"
    assert normalize_business_name("Acme Corporation.") == "acme corp"
    assert normalize_business_name("Global Technologies Limited") == "global tech ltd"
    assert normalize_business_name("Société Anonyme Dufour") == "sa dufour"
    assert normalize_business_name("Müller Technik GmbH") == "muller technik gmbh"
    assert normalize_business_name("Tata Services Pvt Ltd") == "tata services pvt ltd"

def test_address_abbreviation_normalization():
    assert normalize_business_address("100 Main Street") == "100 main st"
    assert normalize_business_address("456 Park Avenue, Apartment 5B") == "456 park ave apt 5b"
    assert normalize_business_address("789 Sunset Boulevard, Suite 100") == "789 sunset blvd ste 100"
    assert normalize_business_address("12 Industrial Road") == "12 industrial rd"

def test_unicode_normalization():
    assert normalize_unicode("Société Généralé") == "Societe Generale"
    assert normalize_unicode("München Straße") == "Munchen Strasse"
    assert normalize_business_name("Café de Paris S.A.") == "cafe de paris sa"

def test_missing_values():
    assert normalize_business_name(None) is None
    assert normalize_business_name(np.nan) is None
    assert normalize_business_address(None) is None
    assert normalize_business_address("") is None
    assert normalize_country(None) is None

def test_country_normalization():
    assert normalize_country("United States") == "US"
    assert normalize_country("USA") == "US"
    assert normalize_country("India") == "IN"
    assert normalize_country("France") == "FR"
    assert normalize_country("Germany") == "DE"
    assert normalize_country("Japan") == "JP"
    assert normalize_country("United Kingdom") == "GB"
    # Test arbitrary / unseen country
    assert normalize_country("New Zealand") == "NEW ZEALAND"
    assert normalize_country("NZ") == "NZ"

def test_id_preservation_and_dataframe_processing():
    raw_data = {
        'entity_id': ['S1_0001', 'S1_0002'],
        'business_name': ['Acme Corporation', 'Société Dufour S.A.'],
        'business_address': ['123 Main Street', None],
        'country': ['United States', 'France']
    }
    df_raw = pd.DataFrame(raw_data)
    df_proc = process_dataframe(df_raw)
    
    # Assert row count preserved
    assert len(df_proc) == 2
    # Assert IDs exact match
    assert list(df_proc['entity_id']) == ['S1_0001', 'S1_0002']
    # Assert canonical columns retained
    assert 'business_name' in df_proc.columns
    assert 'business_address' in df_proc.columns
    assert 'country' in df_proc.columns
    # Assert normalized columns present
    assert df_proc.loc[0, 'business_name_normalized'] == 'acme corp'
    assert df_proc.loc[0, 'business_address_normalized'] == '123 main st'
    assert df_proc.loc[0, 'country_normalized'] == 'US'
    assert df_proc.loc[1, 'business_name_normalized'] == 'societe dufour sa'
    assert pd.isna(df_proc.loc[1, 'business_address_normalized'])
    assert df_proc.loc[1, 'country_normalized'] == 'FR'
