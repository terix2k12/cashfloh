import dataclasses

@dataclasses.dataclass
class Rule:
    condition: str
    action: str
    transformer: str | None = None