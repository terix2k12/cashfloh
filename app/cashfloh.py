# import logging # TODO
import os

from app.core.category_service import CategoryService
from app.core.logic import assign
from app.core.rule_service import RulesService
from app.core.settings import SettingsService
from app.core.writer import saveJson, struc2csv
from app.model.account import Account
from app.model.categories import MISSING
from app.transformers.transformer_dkb import DkbTransformer
from app.transformers.transformer_voba import VobaTransformer


def transform(transformer, categories, rules, f, path):
    print("Applying {} transformer to {}".format(transformer.name, f))
    text = transformer.pdf2text(path)
    # print(text)
    data = transformer.txt2struc(text)
    data.verifystruc()
    assign(rules, data)
    interactive(categories, data)
    return data

def interactive(categories, data: Account):
    for item in data.items:


        if item.main_category == MISSING:
            cats = []
            for value in categories.main_categories.values():
                cats.append(value.name)
            print(f"Main is missing, assign one of {",".join(cats)}")
            item.printItem( 0)
            response = input("Enter to continue...")
            print(f"Assinging {response}")
            item.main_category = response

        if item.sub_category == MISSING:
            subs = []
            for value in categories.sub_categories.values():
                subs.append(value.name)

            print(f"Sub is missing, assign one of {",".join(subs)}")
            item.printItem(0)
            response = input("Enter to continue...")
            print(f"Assinging {response}")
            item.sub_category = response

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
