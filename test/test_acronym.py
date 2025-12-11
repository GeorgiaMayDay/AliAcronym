from logging import Logger

import pytest
from acronym_analysis.acronym_identifier import identify_acronym, fetch_acronym_description, get_acronyms_from_database
from acronym_database.acronym_data import database
from acronym_database.acronym_data_struct import AcronymDataStruct, MultiAcronymDataStruct
from formatters.slack_formatter import clean_str_to_potential_acronyms
from test.utils import test_database

good_acronyms = [
    ("MoD", {"MoD"}),
    ("BERR", {"BERR"}),
    ("MoDD", {"MoDD"}),
    ("MOD BERR", {"MOD", "BERR"}),
    ("U.S.A", {"USA"}),
    ("U.S.A, MoD", {"USA", "MoD"}),
    ("BeDrD", {"BeDrD"}),
    ("We currently have BA's stationed in the U.S.A working on CoW project", {"BA","USA", "CoW"})
]

bad_acronyms = [
    ("BEDrD"),
    ("Cheese"),
]

gov_acronyms = [
    ("MOD", "Ministry of Defence"),
    ("NHS", "National Health Service"),
]

gov_multi_part_acronyms = [
    ("AE", 2, {"AE (education)", "AE (civil service grade)"})
]


sentences_with_acronyms = [
    ("We need to talk this through with the mod", 1,  "Ministry of Defence"),
    ("Interesting, but not sure we want to get A.E. involved this early", 1, ["AE (civil service grade)", "AE (education)"]),
    ("No M.O.D are alot about the A-E program so that needs to be included!", 2, ["Ministry of Defence","AE (civil service grade)", "AE (education)"]),
    ("MOD is MOD, ya know!", 1, ["Ministry of Defence"]),
    ]

@pytest.mark.parametrize("acronym_str, expected", good_acronyms)
def test_identify_acronym_identify_and_passes_back_acronyms(acronym_str, expected):
    assert set(identify_acronym(acronym_str)) == expected

@pytest.mark.parametrize("acronym_str", bad_acronyms)
def test_identify_acronym_identify_return_nothing_when_no_recognised_acronym(acronym_str):
    assert identify_acronym(acronym_str) == []

@pytest.mark.parametrize("acronym_str, expected", gov_acronyms)
def test_fetch_acronym_description_simple_use(acronym_str, expected):
    actual = fetch_acronym_description(acronym_str, curr_database=test_database)
    assert actual.meaning == expected

def test_fetch_acronym_description_repeated_acronyms():
    actual = identify_acronym("MOD, MOD, NHS, AE -- NHS")
    assert len(actual) == 3

def test_fetch_acronym_description_and_no_result_found():
    actual = fetch_acronym_description("BIS", curr_database=test_database)
    assert actual is None

@pytest.mark.parametrize("acronym_str, expected_length, expected_set", gov_multi_part_acronyms)
def test_fetch_acronym_description_multi_depth(acronym_str, expected_length, expected_set):
    actual: MultiAcronymDataStruct = fetch_acronym_description(acronym_str, curr_database=test_database)

    print(actual)

    assert len(actual.acronym_data) == expected_length
    assert set(actual.acronym_data.keys()) == expected_set

@pytest.mark.parametrize("acronym_str, length, expected_meaning", sentences_with_acronyms)
def test_check_whole_string_for_acronym(acronym_str, length, expected_meaning):
    cleaned_sentence = clean_str_to_potential_acronyms(acronym_str)
    actual = get_acronyms_from_database(cleaned_sentence, curr_database=test_database, logger=Logger("test"))

    assert len(actual) == length
    for x in actual:
        if isinstance(x, AcronymDataStruct):
            assert x.meaning in expected_meaning
        else:
            for y in x.acronym_data:
                assert y in expected_meaning