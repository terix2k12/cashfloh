import copy

from cashfloh.model.account import Account
from cashfloh.model.item import AccountItem
from cashfloh.model.rule import Rule
from cashfloh.transformers.transformer import Transformer


class RulesService:

    def validate(self, transformers, categories, rules) -> bool:
        main_categories = [cat.name for cat in categories]
        sub_categories = []
        for cat in categories:
            for sub_cat in cat.sub_categories:
                sub_categories.append(sub_cat.name)
        transformer_ids = [t.id for t in transformers]

        for rule in rules:

            if rule.conditions is None:
                if rule.condition is None or rule.condition == "":
                    raise Exception("Condition cannot be empty")
            else:
                for condition in rule.conditions:
                    # TODO further validation
                    if condition.transformer:
                        if condition.transformer not in transformer_ids:
                            raise Exception("Transformer must be one of {}".format(transformers))

            if rule.action.startswith("ASSIGN"):
                main_category = rule.action.split(".")[1]
                sub_category = rule.action.split(".")[2]
                if (
                    main_category not in main_categories
                    or sub_category not in sub_categories
                ):
                    return False

        return True

    def apply_rule(self, transformer: Transformer, rule: Rule, account: Account, item: AccountItem):
        # TODO loop / and / or
        if rule.actions:
            action = rule.actions[0]
            if action.describe:
                item.description = action.describe
            if action.assign:
                m = action.assign.split(".")[0]
                s = action.assign.split(".")[1]
                item.main_category = m.strip()
                item.sub_category = s.strip()
            if action.split:
                first = float(action.split.split("|")[0])
                second = float(action.split.split("|")[1])
                splitted = action.split.split("|")[2]
                m = splitted.split(".")[0].strip()
                s = splitted.split(".")[1].strip()
                item.value = first
                item_copy = copy.deepcopy(item)
                item_copy.main_category = m
                item_copy.sub_category = s
                item_copy.value = second
                account.items.append(item_copy)
                pass
        pass

    def rule_applies(self, transformer, rule: Rule, item: AccountItem) -> bool:
        # TODO loop / and / or
        if rule.conditions:
            condition = rule.conditions[0]
            if condition.transformer and not transformer.id == condition.transformer:
                return False
            if condition.value and not condition.value == item.value:
                return False
            if condition.debitor and not condition.debitor in item.debitor:
                return False
            return True
        return False

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
