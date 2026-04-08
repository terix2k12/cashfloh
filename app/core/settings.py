import dataclasses
import json
from typing import List


@dataclasses.dataclass
class TransformerSettings:
    type: str
    account: int

@dataclasses.dataclass
class Settings:
    transformers: List[TransformerSettings]


class SettingsService:

    def fromFile(self, path: str) -> Settings:
        with open(path, "r") as file:
            json_object = json.load(file)
            return Settings(**json_object)
