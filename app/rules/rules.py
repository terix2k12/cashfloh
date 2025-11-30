import dataclasses


@dataclasses.dataclass
class Rule:
    id: int
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
            assert len(csv) == 6
            rule_id = int(csv[0])
            debitor = csv[1]
            summary = csv[2]
            details = csv[3]
            short = csv[4]
            action = csv[5]
            rules.append(Rule(rule_id, debitor, summary, details, short, action))
        return rules

    def fromFile(self, path: str):
        with open(path, "r") as file:
            return self.fromText(file.read())
