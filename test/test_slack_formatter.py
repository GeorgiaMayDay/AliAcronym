from logging import Logger
import re

import pytest

from acronym_database.acronym_data_struct import AcronymDataStruct
from formatters.slack_formatter import extract_acronym_and_get_definition, \
    clean_str_to_potential_acronyms, get_acronyms_from_database
from test.utils import test_database

gov_acronyms = [
    ("MoD", "Ministry of defence"),
    ("MOD", "Ministry of Defence"),
    ("BIS", "Sorry"),
    ("NHSx", "Sorry"),
]

gov_multi_part_acronyms = [
    ("AE", ["AE (civil service grade)", "AE (education)"])
]

acronyms_in_sentence = [
    ("Hey, Tony this is really interesting hopefully we'll get this SOW out by EOD tmr", ['EOD', 'HEY', 'HOPEFULLY', 'INTERESTING', 'REALLY', 'SOW', 'TMR', 'TONY', 'WELL']),
    ("Yeah, the MoD really need to get a wiggle on delivering the SAT to the U.S.A", ['DELIVERING', 'MOD', 'NEED', 'REALLY', 'SAT', 'USA', 'WIGGLE', 'YEAH']),
    ("LOL, unnecessary but also ThB", ['ALSO', 'LOL', 'THB', 'UNNECESSARY'])
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

@pytest.mark.parametrize("acronym_str, meaning", acronyms_in_sentence)
def test_acronym_cleaner(acronym_str, meaning):
    actual = clean_str_to_potential_acronyms(acronym_str)
    print(actual)
    assert meaning == actual
