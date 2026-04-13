import dataclasses
import json
from typing import List

from app.model.rule import Rule2


@dataclasses.dataclass
class TransformerSettings:
    type: str
    account: int
    description: str
    name: str

@dataclasses.dataclass
class Settings:
    transformers: List[TransformerSettings]
    rules: List[Rule2]

class SettingsService:

    def fromFile(self, path: str) -> Settings:
        with open(path, "r") as file:
            json_object = json.load(file)
            return Settings(**json_object)
