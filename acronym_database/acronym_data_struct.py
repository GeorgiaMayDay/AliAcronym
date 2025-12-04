from dataclasses import dataclass, asdict


@dataclass
class AcronymDataStruct:
    __slots__ = ("meaning", "description", "department")
    meaning: str
    description: str
    department: str