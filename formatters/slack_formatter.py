import re
import string
from logging import Logger
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


def extract_acronym_and_get_definition(text: str, database: Dict[str, str | Dict[str, str]], logger: Logger) -> List[str]:
    returning_text = []

    acronyms = identify_acronym(text)
    if not acronyms:
        acronyms = clean_str_to_potential_acronyms(text)
        if not acronyms:
            return [f"Sorry, I don't get sent a string"]

    acronym_details = get_acronyms_from_database(acronyms, database, logger)
    acronym_str = ",".join(acronyms)
    if not acronym_details:
        return [f"Sorry, I find any acronyms in the string you sent in my database. You sent: {text}"]
    for acronym in acronym_details:
        output: str| List[str] = determine_output_from_acronym_result(acronym, acronym_str)
        if isinstance(output, str):
            returning_text.append(output)
        else:
            returning_text = returning_text + output
    return returning_text


def determine_output_from_acronym_result(acronym_details: None | AcronymDataStruct | MultiAcronymDataStruct,
                                         acronym_str: str):
    if not acronym_details:
        return f"Sorry, {acronym_str} is not in this database"
    elif isinstance(acronym_details, AcronymDataStruct):
        return acronym_data_string(acronym_details)
    elif isinstance(acronym_details, MultiAcronymDataStruct):
        details = []
        for key, value in acronym_details.acronym_data.items():
            acronym_detail_struct: AcronymDataStruct = AcronymDataStruct(key, **value)
            details.append(acronym_data_string(acronym_detail_struct))
        return details
    else:
        return f"That was weirdly hard: {acronym_details}"


def extract_acronym_description_text(text: str, database: Dict[str, str | Dict[str, str]], logger: Logger) -> str:
    return '\n'.join(extract_acronym_and_get_definition(text, database, logger))


def clean_str_to_potential_acronyms(text: str) -> List[str]:
    # 1. Remove all punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # 2. Upper everything
    text = text.upper()
    # 3. split by whitespace
    potential_acronym_list = text.split(" ")
    return potential_acronym_list


def acronym_data_string(acronym_data: AcronymDataStruct) -> str:
    answer = f"Acronym: {acronym_data.acronym}\n Name: {acronym_data.meaning} \n Description: {acronym_data.description} \n Department: {acronym_data.department}"
    return answer


def get_acronyms_from_database(potential_acronyms: List[str], database: Dict[str, str | Dict[str, str]], logger: Logger) -> List[AcronymDataStruct | MultiAcronymDataStruct]:
    acronyms_in_database = []

    for acronym in potential_acronyms:
        result = fetch_acronym_description(acronym, database)
        if result:
            acronyms_in_database.append(result)

    logger.info(msg="These where the acronym identified")
    logger.info(msg=acronyms_in_database)
    return acronyms_in_database
