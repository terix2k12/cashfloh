import dataclasses

@dataclasses.dataclass
class Rule:
    debitor_keyword: str
    summary_keyword: str
    details_keyword: str
    short_keyword: str
    action: str

class Rule2:
    conditions: list[str]
    actions: list[str]