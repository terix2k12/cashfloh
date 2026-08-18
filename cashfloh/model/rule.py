import dataclasses

@dataclasses.dataclass
class Action:
    assign: str | None = None
    describe: str | None = None
    split: str | None = None

@dataclasses.dataclass
class Condition:
    value: float | None = None
    debitor: str | None = None
    transformer: str | None = None

@dataclasses.dataclass
class Rule:
    # TODO remove legacy condition
    condition: str | None = None
    # TODO remove legacy action
    action: str | None = None

    description: str | None = None
    # TODO improve/implement new properties
    conditions: list[Condition] | None = None
    actions: list[Action] | None = None