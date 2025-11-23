from app.rules.categories import CategoryService


def test_load_default():
    service = CategoryService()
    categories = service.fromFile("default.categories.csv")
    assert categories is not None
    assert len(categories.main_categories) == 2
    assert len(categories.sub_categories) == 5
    pass
