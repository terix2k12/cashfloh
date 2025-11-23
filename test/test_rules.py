from app.rules.rules import RulesService


def test_load_rules():
    service = RulesService()
    rules = service.fromFile("default.rules.csv")
    assert len(rules) == 1
    pass