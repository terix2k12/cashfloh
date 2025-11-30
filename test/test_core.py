from app.core.data import AccountItem, Account
from app.core.logic import assign
from app.rules.categories import CategoryService
from app.rules.rules import RulesService


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
                main="Hobbies",
                sub="a",
                value=123,
                debit="a",
                short="a",
            ),
            AccountItem(
                date="a",
                ktype="a",
                debitor="a",
                summary="a",
                main="a",
                sub="a",
                value=123,
                debit="a",
                short="a",
            ),
            AccountItem(
                date="a",
                ktype="a",
                debitor="a",
                summary="a",
                main="a",
                sub="a",
                value=123,
                debit="a",
                short="a",
            ),
        ],
    )
    output_data = assign(categories, rules, input_data)

    assert output_data is not None
    assert output_data.items[0].main == "Hobbies"
