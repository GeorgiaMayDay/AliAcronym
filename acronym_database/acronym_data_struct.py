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
    __slots__ = "acronym_data"
    acronym_data: Dict[str, AcronymDataStruct]