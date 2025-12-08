import pytest

from formatters.slack_formatter import extract_acronym_and_get_definition

test_database = {
    "MOD": {
        "meaning": "Ministry of Defence",
        "description": "",
        "department": "MoD"
    },
    "MoD": {
        "meaning": "Ministry of defence",
        "description": "",
        "department": "MoD"
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


gov_acronyms = [
    ("MoD", " Name: Ministry of defence "),
    ("MOD", " Name: Ministry of Defence "),
    ("BIS", "Sorry, BIS is not in this database"),
    ("NHS", "Sorry, NHS is not in this database"),
]

gov_multi_part_acronyms = [
    ("AE", 2, {"AE (education)", "AE (civil service grade)"})
]

@pytest.mark.parametrize("acronym_str, expected", gov_acronyms)
def test_identify_acronym_identify_and_passes_back_acronyms(acronym_str, expected):
    actual = extract_acronym_and_get_definition(acronym_str, database=test_database)[0].split('\n')

    assert expected in actual

@pytest.mark.parametrize("acronym_str, length, set", gov_multi_part_acronyms)
def test_identify_acronym_identify_and_passes_back_acronyms(acronym_str, length, set):
    actual = extract_acronym_and_get_definition(acronym_str, database=test_database)

    assert length == len(actual)