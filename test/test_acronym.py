import pytest
from acronym_analysis.acronym_identifier import identify_acronym, fetch_acronym_description
from acronym_database.acronym_data import database
from acronym_database.acronym_data_struct import AcronymDataStruct, MultiAcronymDataStruct

test_database = {
    "MoD": {
        "meaning": "Ministry of Defence",
        "description": "",
        "department": "MoD"
    },
    "NHS":{
        "meaning": "National Health Service",
        "description": "",
        "department": "NHS"
    },
    "AE": {
    "AE (civil service grade)": {
        "meaning": "Assistant Economists",
        "description": "",
        "department": "Civil Service Wide"
    },
        "AE (education)": {
            "meaning": "Adult education",
            "description": "",
            "department": "DfE"
        }
    },
}

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
    ("NHS", "National Health Service"),
]

gov_multi_part_acronyms = [
    ("AE", 2, {"AE (education)", "AE (civil service grade)"})
]
@pytest.mark.parametrize("acronym_str, expected", good_acronyms)
def test_identify_acronym_identify_and_passes_back_acronyms(acronym_str, expected):
    assert identify_acronym(acronym_str) == expected

@pytest.mark.parametrize("acronym_str", bad_acronyms)
def test_identify_acronym_identify_return_nothing_when_no_recognised_acronym(acronym_str):
    assert identify_acronym(acronym_str) == []

@pytest.mark.parametrize("acronym_str, expected", gov_acronyms)
def test_fetch_acronym_description_simple_use(acronym_str, expected):
    actual = fetch_acronym_description(acronym_str, database=test_database)
    assert actual.meaning == expected

def test_fetch_acronym_description_and_no_result_found():
    actual = fetch_acronym_description("BIS", database=test_database)
    assert actual is None

@pytest.mark.parametrize("acronym_str, expected_length, expected_set", gov_multi_part_acronyms)
def test_fetch_acronym_description_multi_depth(acronym_str, expected_length, expected_set):
    actual: MultiAcronymDataStruct = fetch_acronym_description(acronym_str, database=test_database)

    print(actual)

    assert len(actual.acronym_data) == expected_length
    assert set(actual.acronym_data.keys()) == expected_set