import dataclasses

from dataclasses_json import dataclass_json

from cashfloh.model.categories import MainCategory
from cashfloh.model.rule import Rule


@dataclasses.dataclass
class TransformerSettings:
    type: str
    account: int
    description: str
    name: str
    id: str

@dataclass_json
@dataclasses.dataclass
class Settings:
    main_categories: list[MainCategory]
    transformers: list[TransformerSettings]
    rules: list[Rule]

class SettingsService:

    def fromFile(self, path: str) -> Settings:
        with open(path + ".settings.json", "r") as file:
            return Settings.from_json(file.read())
