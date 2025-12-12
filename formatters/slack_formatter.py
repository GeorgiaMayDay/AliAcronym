import logging
import re
import string
from logging import Logger
from typing import Dict, List

from acronym_analysis.acronym_identifier import identify_acronym, get_acronyms_from_database
from acronym_database.acronym_data import database
from acronym_database.acronym_data_struct import AcronymDataStruct, MultiAcronymDataStruct
from constants import common_words


def friendly_response(text: str,  msg_type: str = "") -> str:
    returning_text = ""
    match msg_type:
        case "mention":
            returning_text = "I've analysis the parent message and found the following acronyms:\n"
        case _:
            returning_text = "Here are the acronyms I have found: \n"
    analysis_response = extract_acronym_description_text(text, database=database)
    return returning_text + analysis_response


def extract_acronym_and_get_definition(text: str, database: Dict[str, str | Dict[str, str]], logger: Logger = logging.getLogger("task")) -> List[str]:
    if logger.level == logging.NOTSET:
        logger.setLevel(logging.INFO)
    returning_text = []

    acronyms = identify_acronym(text)
    if not acronyms:
        acronyms = clean_str_to_potential_acronyms(text)
        if not acronyms:
            return [f"Sorry, I don't get sent a string"]

    acronym_details = get_acronyms_from_database(acronyms, database, logger)
    acronym_str = ",".join(acronyms)

    logging.info(msg="Identified acronyms:"+ acronym_str)

    if not acronym_details:
        return [f"Sorry, I find any acronyms in the string you sent in my database. You sent: {text}"]
    for acronym in acronym_details:
        output: str| List[str] = determine_output_from_acronym_result(acronym, acronym_str)
        if isinstance(output, str):
            returning_text.append(output)
        else:
            returning_text.append("\n\n".join(output))
    return returning_text


def determine_output_from_acronym_result(acronym_details: None | AcronymDataStruct | MultiAcronymDataStruct,
                                         acronym_str: str):
    if not acronym_details:
        return f"Sorry, {acronym_str} is not in this database"
    elif isinstance(acronym_details, AcronymDataStruct):
        return acronym_data_details_string(acronym_details)
    elif isinstance(acronym_details, MultiAcronymDataStruct):
        details = [
            f"I recognise this acronym ({acronym_details.acronym}) as having multiple potential meanings. Let me go through them: "]
        for key, value in acronym_details.acronym_data.items():
            acronym_detail_struct: AcronymDataStruct = AcronymDataStruct(key, **value)
            details.append(acronym_data_details_string(acronym_detail_struct))
        return details
    else:
        return f"500: Database Error on: {acronym_details}"


def extract_acronym_description_text(text: str, database: Dict[str, str | Dict[str, str]]) -> str:
    return '\n\n'.join(extract_acronym_and_get_definition(text, database))


def clean_str_to_potential_acronyms(text: str) -> List[str]:
    # 1. Remove all punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # 2. remove words that are very likely to just be filler words and turn into list
    potential_acronym_list = [word for word in re.split("\W+", text) if word not in common_words]
    # 3. upper everything
    potential_acronym_list = map(lambda x: x.upper(), potential_acronym_list)
    # 4. Make sure that all the words are unique and sort the list
    return sorted(list(set(potential_acronym_list)))


def acronym_data_details_string(acronym_data: AcronymDataStruct) -> str:
    description = acronym_data.description if acronym_data.description else "Unfortunately, I don't have a description."
    department = acronym_data.department if acronym_data.department else "CS Wide"
    answer = f" {acronym_data.acronym} means {acronym_data.meaning}. {description} And it's used in the {department}"
    return answer


