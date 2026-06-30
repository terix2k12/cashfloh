from cashfloh.model.account import Account
from cashfloh.model.item import AccountItem
from cashfloh.model.rule import Rule


def assign(rules: list[Rule], input_data: Account):
    for item in input_data.items:
        for rule in rules:
            # TODO do verification at startup
            if rule.condition is None or rule.condition == "":
                raise Exception("Condition cannot be empty")
            if rule.condition in item.debitor:
                applyRule(item, rule)
            for text in item.texts:
                if rule.condition in text:
                    applyRule(item, rule)
    return input_data


def applyRule(item: AccountItem, rule: Rule):
    if rule.action.startswith('ASSIGN'):
        m = rule.action.split(".")[1]
        s = rule.action.split(".")[2]
        item.main_category = m
        item.sub_category = s
    if rule.action.startswith('DETAILS'):
        item.details = rule.action.split("=")[1]


def assignCategories(data):

    c = 1
    for item in data["items"]:
        (main, sub) = extractCategory(item["debitor"], item["summary"])

        if main == 0 or sub == 0:
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
    main = 0
    sub = 0
    return (main, sub)
