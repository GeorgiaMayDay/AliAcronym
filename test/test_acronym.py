import pytest
from acronym_analysis.acronym_identifier import identify_acronym, fetch_acronym_description
from acronym_database.acronym_data_struct import AcronymDataStruct

good_acronyms = [
    ("MoD", ["MoD"]),
    ("BERR", ["BERR"]),
    ("MoDD", ["MoDD"]),
    ("MOD BERR", ["MOD", "BERR"]),
    ("U.S.A", ["U.S.A"]),
    ("U.S.A, MoD", ["U.S.A", "MoD"]),
    ("BeDrD", ["BeDrD"]),
    ("We currently have BA's stationed in the U.S.A working on CoW project", ["BA","U.S.A", "CoW"])
]

bad_acronyms = [
    ("BEDrD"),
    ("Cheese"),
]

@pytest.mark.parametrize("acronym_str, expected", good_acronyms)
def test_identify_acronym_identify_and_passes_back_acronyms(acronym_str, expected):
    assert identify_acronym(acronym_str) == expected

@pytest.mark.parametrize("acronym_str", bad_acronyms)
def test_identify_acronym_identify_return_nothing_when_no_recognised_acronym(acronym_str):
    assert identify_acronym(acronym_str) == []

def test_fetch_acronym_description():
    assert fetch_acronym_description("MOD") == AcronymDataStruct(meaning="cheese", description='delicious', department="MOD")