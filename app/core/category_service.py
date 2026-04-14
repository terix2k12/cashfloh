from app.core.settings import Settings


class CategoryService:

    def verify(self, settings: Settings) -> bool:
        # TODO
        return True

    # def fromText(self, text: str) -> Categories:
    #     cat = Categories()
    #     for line in text.splitlines():
    #         if line.startswith("#"):
    #             continue
    #         csv = line.split(";")
    #         assert len(csv) == 3
    #         cat_id = int(csv[0])
    #         sub_id = int(csv[1])
    #         name = csv[2]
    #         if sub_id == 0:
    #             cat.main_categories[cat_id] = MainCategory(cat_id, name, "", [])
    #             assert cat_id > 0
    #         else:
    #             assert cat_id in cat.main_categories
    #             cat.sub_categories[sub_id] = SubCategory(sub_id, name, "", cat_id)
    #     return cat
    #
    # def fromFile(self, path: str) -> Categories:
    #     with open(path, "r") as file:
    #         return self.fromText(file.read())