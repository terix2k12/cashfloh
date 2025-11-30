# import logging # TODO
import os

from app.core.logic import assign
from app.rules.categories import CategoryService
from app.rules.rules import RulesService
from app.transformers.transformer_dkb import DkbTransformer
from app.transformers.transformer_voba import VobaTransformer


def main(categories_path, rules_path, inputpath):

    categories = CategoryService().fromFile(categories_path)
    rules = RulesService().fromFile(rules_path)

    transformers = [DkbTransformer(), VobaTransformer()]

    for dirpath, dnames, fnames in os.walk(inputpath):
        for f in fnames:
            path = os.path.join(dirpath, f)
            print("Processing {}".format(path))
            for transformer in transformers:
                if transformer.checkFilename(f):
                    print("Applying {} transformer to {}".format(transformer.name, f))
                    text = transformer.pdf2text(path)
                    # print(text)
                    data = transformer.txt2struc(text)
                    ok = data.verifystruc()
                    if not ok:
                        data.printstruc()
                    else:
                        assign(categories, rules, data)
                        # writer.saveJson(json_path, data)
                        # writer.struc2csv(csv_path, data)
                else:
                    print("Skipping {} transformer to {}".format(transformer.name, f))
    pass
