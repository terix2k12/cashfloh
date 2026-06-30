import dataclasses

@dataclasses.dataclass
class SubCategory:
    name: str
    hotkey: str


@dataclasses.dataclass
class MainCategory:
    name: str
    hotkey: str
    sub_categories: list[SubCategory]

