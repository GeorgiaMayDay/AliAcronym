import string
from typing import List
import re

from acronym_database.acronym_data_struct import AcronymDataStruct

# Check tests for this
# Should accept as acronym: Any all capital string, and
acronym_pattern = r"\b(?:[A-Z]{2,}[:alpha:]*)|(?:[A-Z][a-z][A-Z][A-Za-z]*)|(?:[a-zA-Z]\.){2|(?:[a-zA-Z]\.){2,}[a-zA-Z]"

def findWholeWord(w, s):
    for p in [*string.whitespace, *string.punctuation]:
        if (' ' + w + p) in (' ' + s + p):
            return True
    return None


def identify_acronym(acronym: str) -> List[str]:
    final_acronyms = []
    initial_acronym_scan = re.findall(acronym_pattern, acronym)
    for acr in initial_acronym_scan:
        if findWholeWord(acr, acronym):
            final_acronyms.append(acr)
    return final_acronyms

def fetch_acronym_description(acronym: str) -> AcronymDataStruct:
    return AcronymDataStruct(meaning="cheese", description='delicious', department=acronym)

