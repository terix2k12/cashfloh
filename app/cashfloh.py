# import logging # TODO
import os

from app.core.logic import assign
from app.core.settings import SettingsService
from app.core.writer import saveJson, struc2csv
from app.rules.categories import CategoryService
from app.rules.rules import RulesService
from app.transformers.transformer_dkb import DkbTransformer
from app.transformers.transformer_voba import VobaTransformer


def transform(transformer, categories, rules, f, path):
    print("Applying {} transformer to {}".format(transformer.name, f))
    text = transformer.pdf2text(path)
    # print(text)
    data = transformer.txt2struc(text)
    ok = data.verifystruc()
    if not ok:
        data.printstruc()
    else:
        assign(categories, rules, data)
    return data

def handleFile():
    # TODO
    pass

def handleFolder():
    # TODO
    pass

def main(settings_path, categories_path, rules_path, inputpath):

    categories = CategoryService().fromFile(categories_path)
    rules = RulesService().fromFile(rules_path)
    settings = SettingsService().fromFile(settings_path)

    transformers = [DkbTransformer(settings.transformers), VobaTransformer(settings.transformers)]

    for dirpath, dnames, fnames in os.walk(inputpath):
        for f in fnames:
            if not f.endswith(".pdf"):
                continue
            path = os.path.join(dirpath, f)
            print("Processing {}".format(path))
            for transformer in transformers:
                if transformer.checkFilename(f):
                    data = transform(transformer, categories, rules, f, path)
                    json_path = os.path.join(dirpath, f[:-4] + ".json")
                    csv_path = os.path.join(dirpath, f[:-4] + ".csv")
                    saveJson(json_path, data)
                    struc2csv(csv_path, data)
                else:
                    print("Skipping {} transformer to {}".format(transformer.name, f))
    pass
