from typing import Dict, List

from acronym_analysis.acronym_identifier import identify_acronym, fetch_acronym_description
from acronym_database.acronym_data import database
from acronym_database.acronym_data_struct import AcronymDataStruct, MultiAcronymDataStruct


def get_acronym(text: str) -> str:
    acronyms = identify_acronym(text)
    if acronyms:
        return f"I've identified:{acronyms} \n That's a nice acronym"
    else:
        return f"I'm sorry I couldn't find an acronym in the string you sent me"

def extract_acronym_and_get_definition(text: str, database: Dict[str, str | Dict[str, str]]) -> List[str]:
    returning_text = []
    acronyms = identify_acronym(text)
    acronym_str = ",".join(acronyms)
    if not acronyms:
        return ["Sorry I couldn't find an acronym in the string you sent me"]
    for acronym in acronyms:
        acronym_details = fetch_acronym_description(acronym, database=database)
        if not acronym_details:
            returning_text.append(f"Sorry, {acronym_str} is not in this database")
        elif isinstance(acronym_details, AcronymDataStruct):
            returning_text.append(acronym_data_string(acronym_details))
        elif isinstance(acronym_details, MultiAcronymDataStruct):
            for key, value in acronym_details.acronym_data.items():
                acronym_detail_struct: AcronymDataStruct = AcronymDataStruct(key, **value)
                returning_text.append(acronym_data_string(acronym_detail_struct))
        else:
            returning_text.append(f"That was weirdly hard: {acronym}, {acronym_details}")
    return returning_text

def extract_acronym_description_text(text: str, database: Dict[str, str | Dict[str, str]]) -> str:
    return '\n'.join(extract_acronym_and_get_definition(text, database))

def clean(text: str) -> str:
    text = text.replace("\n", " ")

def acronym_data_string(acronym_data: AcronymDataStruct) -> str:
    answer = f"Acronym: {acronym_data.acronym}\n Name: {acronym_data.meaning} \n Description: {acronym_data.description} \n Department: {acronym_data.department}"
    return answer