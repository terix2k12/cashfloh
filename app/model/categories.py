import dataclasses

MISSING = 0

@dataclasses.dataclass
class SubCategory:
    id: int
    name: str
    hotkey: str
    parent: int


@dataclasses.dataclass
class MainCategory:
    id: int
    name: str
    hotkey: str
    sub_categories: list[SubCategory]


class Categories:
    main_categories: dict[int, MainCategory] = {}
    sub_categories: dict[int, SubCategory] = {}

