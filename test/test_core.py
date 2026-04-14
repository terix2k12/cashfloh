from cashfloh.core.data import AccountItem, Account
from cashfloh.rules.categories import CategoryService
from cashfloh.rules.rule_service import RulesService

from cashfloh.core.logic import assign


def test_core():
    rules = RulesService().fromFile("default.rules.csv")
    categories = CategoryService().fromFile("default.categories.csv")

    input_data = Account(
        kontoauszug="a",
        startSaldo=456,
        endSaldo=789,
        items=[
            AccountItem(
                date="a",
                ktype="a",
                debitor="a",
                summary="a",
                main_category="Hobbies",
                sub_category="a",
                value=123,
                debit="a",
                short="a",
            ),
            AccountItem(
                date="a",
                ktype="a",
                debitor="a",
                summary="a",
                main_category="a",
                sub_category="a",
                value=123,
                debit="a",
                short="a",
            ),
            AccountItem(
                date="a",
                ktype="a",
                debitor="a",
                summary="a",
                main_category="a",
                sub_category="a",
                value=123,
                debit="a",
                short="a",
            ),
        ],
    )
    output_data = assign(categories, rules, input_data)

    assert output_data is not None
    assert output_data.items[0].main_category == "Hobbies"
