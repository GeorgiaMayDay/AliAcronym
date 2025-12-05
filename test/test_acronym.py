import pytest
from acronym_analysis.acronym_identifier import identify_acronym, fetch_acronym_description
from acronym_database.acronym_data_struct import AcronymDataStruct

# This is all currently tested against the real database
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

gov_acronyms = [
    ("MoD", "Ministry of Defence"),
    ("MOD", "Ministry of Defence"),
    ("BIS", "Department for Business, Innovation and Skills"),
    ("NHS", "National Health Service"),
]

gov_multi_part_acronyms = [

]
@pytest.mark.parametrize("acronym_str, expected", good_acronyms)
def test_identify_acronym_identify_and_passes_back_acronyms(acronym_str, expected):
    assert identify_acronym(acronym_str) == expected

@pytest.mark.parametrize("acronym_str", bad_acronyms)
def test_identify_acronym_identify_return_nothing_when_no_recognised_acronym(acronym_str):
    assert identify_acronym(acronym_str) == []

@pytest.mark.parametrize("acronym_str, expected", gov_acronyms)
def test_fetch_acronym_description_simple_use(acronym_str, expected):
    actual = fetch_acronym_description(acronym_str)
    assert actual.meaning == expected

@pytest.mark.parametrize("acronym_str, expected", gov_acronyms)
def test_fetch_acronym_description_multi_depth(acronym_str, expected):
    actual = fetch_acronym_description(acronym_str)
    assert actual.acronym == expected