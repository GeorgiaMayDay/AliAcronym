from typing import List
import re
# Check tests for this
# Should accept as acronym: Any all capital string, and
acronym_pattern = r"\b(?:[A-Z]{2,}[:alpha:]*)|(?:[A-Z][a-z][A-Z][:alpha:]*)|(?:[a-zA-Z]\.){2|(?:[a-zA-Z]\.){2,}[a-zA-Z]"

def identify_acronym(acronym: str) -> List[str]:
    return re.findall(acronym_pattern, acronym)