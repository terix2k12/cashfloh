from cashfloh.rules.categories import CategoryService
from cashfloh.rules.rule_service import RulesService


def test_load_default_rules():
    service = RulesService()
    rules = service.fromFile("default.rules.csv")
    assert len(rules) == 3
    pass


def test_validate_default_rules():
    service = RulesService()
    rules = service.fromFile("default.rules.csv")
    categories = CategoryService().fromFile("default.categories.csv")
    assert service.validate([], categories, rules)
    pass
