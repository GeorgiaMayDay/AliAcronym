from logging import Logger
import re

import pytest

from acronym_database.acronym_data_struct import AcronymDataStruct
from formatters.slack_formatter import extract_acronym_and_get_definition, \
    clean_str_to_potential_acronyms, get_acronyms_from_database

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
    ("MoD", "Ministry of defence"),
    ("MOD", "Ministry of Defence"),
    ("BIS", "Sorry"),
    ("NHS", "Sorry"),
]

gov_multi_part_acronyms = [
    ("AE", ["AE (civil service grade)", "AE (education)"])
]

sentences_with_acronyms = [
    ("We need to talk this through with the mod", 1,  "Ministry of Defence"),
    ("Interesting, but not sure we want to get A.E. involved this early", 1, ["AE (civil service grade)", "AE (education)"]),
    ("No M.O.D are alot about the A-E program so that needs to be included!", 2, ["Ministry of Defence","AE (civil service grade)", "AE (education)"])
    ]

@pytest.mark.parametrize("acronym_str, expected", gov_acronyms)
def test_identify_acronym_and_passes_back_acronyms_details(acronym_str, expected):
    actual = extract_acronym_and_get_definition(acronym_str, database=test_database, logger=Logger("test"))

    assert re.findall(expected, actual[0])

@pytest.mark.parametrize("acronym_str, meaning", gov_multi_part_acronyms)
def test_identify_acronym_identify_and_passes_back_acronyms_multi_part(acronym_str, meaning):
    actual = extract_acronym_and_get_definition(acronym_str, database=test_database, logger=Logger("test"))
    print(actual)
    assert meaning[0] in actual[0]
    assert meaning[1] in actual[0]

@pytest.mark.parametrize("acronym_str, length, expected_meaning", sentences_with_acronyms)
def test_check_whole_string_for_acronym(acronym_str, length, expected_meaning):
    cleaned_sentence = clean_str_to_potential_acronyms(acronym_str)
    actual = get_acronyms_from_database(cleaned_sentence, database=test_database, logger=Logger("test"))

    assert len(actual) == length
    for x in actual:
        if isinstance(x, AcronymDataStruct):
            assert x.meaning in expected_meaning
        else:
            for y in x.acronym_data:
                assert y in expected_meaning