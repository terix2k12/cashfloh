import dataclasses


@dataclasses.dataclass
class Rule:
    debitor_keyword: str
    summary_keyword: str
    details_keyword: str
    short_keyword: str
    action: str


class RulesService:

    def validate(self, categories, rules) -> bool:
        main_categories = [cat.name for cat in categories.main_categories.values()]
        sub_categories = [cat.name for cat in categories.sub_categories.values()]
        for rule in rules:
            if rule.action.startswith("ASSIGN"):
                main_category = rule.action.split(".")[1]
                sub_category = rule.action.split(".")[2]
                if (
                    main_category not in main_categories
                    or sub_category not in sub_categories
                ):
                    return False
        return True

    def fromText(self, text: str):
        rules = []
        for line in text.splitlines():
            if line.startswith("#"):
                continue
            csv = line.split(";")
            assert len(csv) == 5
            debitor = csv[0].replace('"', "")
            summary = csv[1]
            details = csv[2]
            short = csv[3].replace('"', "")
            action = csv[4].replace('"', "")
            rules.append(Rule(debitor, summary, details, short, action))
        return rules

    def fromFile(self, path: str):
        with open(path, "r") as file:
            return self.fromText(file.read())
