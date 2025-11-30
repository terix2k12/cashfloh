from app.rules.categories import MISSING


def assign(categories, rules, input_data):
    return input_data


def assignCategories(data):

    c = 1
    for item in data["items"]:
        (main, sub) = extractCategory(item["debitor"], item["summary"])

        if main == MISSING or sub == MISSING:
            print("Can´t assign category")
            printItem(item, c)

            for t in list(MainCategory):
                print(f" {t} {t.value} ")
            m = input("Choose main category:\n")
            main = MainCategory(int(m))
            print(f"Selected {main}")

            for t in list(SubCategory):
                print(f" {t} {t.value} ")
            m = input("Choose sub category:\n")
            sub = SubCategory(int(m))
            print(f"Selected {sub}")

        item["main"] = main
        item["sub"] = sub

        c += 1


def extractCategory(debitor, description):
    main = MISSING
    sub = MISSING
    return (main, sub)
