import dataclasses

MISSING = 0


@dataclasses.dataclass
class MainCategory:
    id: int
    name: str


@dataclasses.dataclass
class SubCategory:
    id: int
    name: str
    parent: int


class Categories:
    main_categories: dict[int, MainCategory] = {}
    sub_categories: dict[int, SubCategory] = {}

