from app.core.data import Account, AccountItem
from app.rules.categories import MISSING
from app.rules.rules import Rule


def assign(categories, rules: list[Rule], input_data: Account):
    c = 1
    for item in input_data.items:
        for rule in rules:
            if rule.debitor_keyword is not "":
                if rule.debitor_keyword in item.debitor:
                    applyRule(item, rule)
            if rule.short_keyword is not "":
                if rule.short_keyword in item.summary:
                    applyRule(item, rule)
        c += 1
    return input_data


def applyRule(item: AccountItem, rule):
    if rule.action.startswith('ASSIGN'):
        m = rule.action.split(".")[1]
        s = rule.action.split(".")[2]
        item.main = m
        item.sub = s
    if rule.action.startswith('DETAILS'):
        item.details = rule.action.split("=")[1]


def assignCategories(data):

    c = 1
    for item in data["items"]:
        (main, sub) = extractCategory(item["debitor"], item["summary"])

        if main == MISSING or sub == MISSING:
            print("Can´t assign category")
    #        printItem(item, c)

   #         for t in list(MainCategory):
#                print(f" {t} {t.value} ")
            m = input("Choose main category:\n")
  #          main = MainCategory(int(m))
            print(f"Selected {main}")

 #           for t in list(SubCategory):
 #               print(f" {t} {t.value} ")
            m = input("Choose sub category:\n")
#            sub = SubCategory(int(m))
            print(f"Selected {sub}")

  #      item["main"] = main
   #     item["sub"] = sub

        c += 1


def extractCategory(debitor, description):
    main = MISSING
    sub = MISSING
    return (main, sub)
