import dataclasses

@dataclasses.dataclass
class Rule:
    condition: str
    action: str