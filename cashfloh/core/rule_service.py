from cashfloh.model.rule import Rule


class RulesService:

    def validate(self, transformers, categories, rules) -> bool:
        main_categories = [cat.name for cat in categories]
        sub_categories = []
        for cat in categories:
            for sub_cat in cat.sub_categories:
                sub_categories.append(sub_cat.name)
        transformer_ids = [t.id for t in transformers]
        for rule in rules:
            if rule.condition is None or rule.condition == "":
                raise Exception("Condition cannot be empty")
            if rule.action.startswith("ASSIGN"):
                main_category = rule.action.split(".")[1]
                sub_category = rule.action.split(".")[2]
                if (
                    main_category not in main_categories
                    or sub_category not in sub_categories
                ):
                    return False
            if rule.transformer:
                if rule.transformer not in transformer_ids:
                    raise Exception("Transformer must be one of {}".format(transformers))
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
