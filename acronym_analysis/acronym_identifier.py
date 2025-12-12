import string
from logging import Logger
from typing import List, Dict
import re

from acronym_database.acronym_data_struct import AcronymDataStruct, MultiAcronymDataStruct

# Should accept as acronym: Any all capital string, any word broken up by full-stops, and words with multiple capital letters with lower case inbetween
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
            acr = acr.translate(str.maketrans('', '', string.punctuation))
            final_acronyms.append(acr)
    # The database has no acronyms presented as U.H so we strip . out
    return list(set(final_acronyms))


def fetch_acronym_description(acronym: str, curr_database: Dict[str, str | Dict[str, str]]) -> None | AcronymDataStruct | MultiAcronymDataStruct:
    acronym_data: Dict = curr_database.get(acronym)
    if not acronym_data:
        return None
    try:
        return AcronymDataStruct(acronym, **acronym_data)
    except TypeError:
        print(acronym_data)
        return MultiAcronymDataStruct(acronym=acronym, acronym_data=acronym_data)

def get_acronyms_from_database(potential_acronyms: List[str], curr_database: Dict[str, str | Dict[str, str]], logger: Logger) -> List[AcronymDataStruct | MultiAcronymDataStruct]:
    acronyms_in_database = []

    for acronym in potential_acronyms:
        result = fetch_acronym_description(acronym, curr_database)
        if result:
            acronyms_in_database.append(result)

    logger.info(msg="These where the acronym identified")
    logger.info(msg=acronyms_in_database)
    return acronyms_in_database
