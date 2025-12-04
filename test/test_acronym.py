import pytest
from acronym_analysis.acronym_identifier import identify_acronym

good_acronyms = [
    ("MoD", ["MoD"]),
    ("BERR", ["BERR"]),
    ("MoDD", ["MoDD"]),
    ("MOD BERR", ["MOD", "BERR"]),
    ("U.S.A", ["U.S.A"]),
    ("U.S.A, MoD", ["U.S.A", "MoD"])
]

bad_acronyms = [
    ("BEDrD", ["BEDrR"]),
    ("BeDrD", ["BeDrR"]),
]

@pytest.mark.parametrize("acronym_str, expected", good_acronyms)
def test_identify_acronym_identify_and_passes_back_acronyms(acronym_str, expected):
    assert identify_acronym(acronym_str) == expected