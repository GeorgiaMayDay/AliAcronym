from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class AcronymDataStruct:
    __slots__ = ("acronym", "meaning", "description", "department")
    acronym: str
    meaning: str
    description: str
    department: str

@dataclass
class MultiAcronymDataStruct:
    __slots__ = ("acronym", "acronym_data")
    acronym: str
    acronym_data: Dict[str, AcronymDataStruct]