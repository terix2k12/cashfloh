import dataclasses

from dataclasses_json import dataclass_json

from app.model.categories import MainCategory
from app.model.rule import Rule2


@dataclasses.dataclass
class TransformerSettings:
    type: str
    account: int
    description: str
    name: str

@dataclass_json
@dataclasses.dataclass
class Settings:
    main_categories: list[MainCategory]
    transformers: list[TransformerSettings]
    rules: list[Rule2]

class SettingsService:

    def fromFile(self, path: str) -> Settings:
        with open(path, "r") as file:
            return Settings.from_json(file.read())
            #json_object = json.load(file)
            #return Settings(**json_object)
