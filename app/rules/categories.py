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

class Categories:
    main_categories: dict[int, MainCategory] = {}
    sub_categories:dict[int, SubCategory] = {}

class CategoryService:

    def fromText(self, text: str):
        cat = Categories()
        for line in text.splitlines():
            if line.startswith("#"):
                continue
            csv = line.split(";")
            assert len(csv) == 3
            id = int(csv[0])
            sub_id = int(csv[1])
            name = csv[2]
            if id > 0:
                cat.main_categories[id] = MainCategory(id, name)
            if sub_id > 0:
                cat.sub_categories[sub_id] = SubCategory(sub_id, name)

        return cat

    def fromFile(self, path: str):
        with open(path, "r") as file:
            return self.fromText(file.read())
