import dataclasses


@dataclasses.dataclass
class Rule:
    id: int
    keyword: str
    action: str


class RulesService:

    def fromText(self, text: str):
        rules = []
        for line in text.splitlines():
            if line.startswith("#"):
                continue
            csv = line.split(";")
            assert len(csv) == 3
            id = int(csv[0])
            keyword = csv[1]
            action = csv[2]
            rules.append(Rule(id, keyword, action))

        return rules

    def fromFile(self, path: str):
        with open(path, "r") as file:
            return self.fromText(file.read())
