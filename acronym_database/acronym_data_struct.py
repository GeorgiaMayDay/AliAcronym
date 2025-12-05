from dataclasses import dataclass, asdict
from typing import List


@dataclass
class AcronymDataStruct:
    __slots__ = ("acronym", "meaning", "description", "department")
    acronym: str
    meaning: str
    description: str
    department: str

@dataclass
class MultiAcronymDataStruct:
    __slots__ = "acronym_data"
    acronym_data: List[AcronymDataStruct]