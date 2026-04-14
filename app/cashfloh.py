# import logging # TODO
import os

from app.core.category_service import CategoryService
from app.core.logic import assign
from app.core.settings import SettingsService
from app.core.writer import saveJson, struc2csv
from app.model.account import Account
from app.model.categories import MISSING, MainCategory, SubCategory
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


def interactive(categories: list[MainCategory], data: Account):
    for item in data.items:

        if item.main_category == MISSING:
            cats = []
            for value in categories:
                cats.append(f"{value.name}({value.hotkey})")

            item.printItem(0)
            cx: MainCategory | None = None
            while cx is None:
                response = input(f"Category is missing, assign one of: {", ".join(cats)}")
                if len(response):
                    cx = next(filter(lambda c: c.hotkey == response, categories), None)
                else:
                    break

            if cx:
                item.main_category = cx

                if item.sub_category == MISSING:

                    subs = []
                    for value in cx.sub_categories:
                        subs.append(f"{value.name}({value.hotkey})")

                    cy: SubCategory | None = None
                    while cy is None:
                        response = input(f"Subcategory is missing, assign one of: {", ".join(subs)}")
                        if len(response):
                            cy = next(filter(lambda c: c.hotkey == response, cx.sub_categories), None)
                        else:
                            break

                    if cy:
                        print(f"Assigned {cx.name} {cy.name}")
                        item.sub_category = cy


def main(settings_path, inputpath):
    # TODO verify? rules = RulesService().fromFile(rules_path)

    settings = SettingsService().fromFile(settings_path)
    CategoryService().verify(settings.main_categories)

    # TODO fix dynamic Transformers
    transformers = [
        DkbTransformer(settings.transformers),
        DkbTransformer(settings.transformers),
        VobaTransformer(settings.transformers)
    ]

    for dirpath, dnames, fnames in os.walk(inputpath):
        for f in fnames:
            if not f.endswith(".pdf"):
                continue
            path = os.path.join(dirpath, f)
            print("Processing {}".format(path))
            for transformer in transformers:
                if transformer.checkFilename(f):
                    data = transform(transformer, settings.main_categories, settings.rules, f, path)
                    json_path = os.path.join(dirpath, f[:-4] + ".json")
                    csv_path = os.path.join(dirpath, f[:-4] + ".csv")
                    saveJson(json_path, data)
                    struc2csv(csv_path, data)
                else:
                    print("Skipping {} transformer to {}".format(transformer.name, f))
    pass
