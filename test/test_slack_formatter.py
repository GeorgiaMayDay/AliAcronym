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

