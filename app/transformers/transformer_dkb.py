import re
from typing import List

from app.core.settings import TransformerSettings
from app.model.account import Account
from app.model.categories import MISSING
from app.model.item import AccountItem
from app.transformers.transformer import Transformer


class DkbTransformer(Transformer):

    type: str = "DkbTransformer"
    name: str
    kontonr: str
    description: str

    def __init__(self, settings: List[TransformerSettings]):
        config = list(filter(lambda p: p.type == self.type, settings))
        assert len(config) == 1
        self.kontonr = config[0].account
        self.name = config[0].name
        self.description = config[0].description

    def checkFilename(self, filename) -> bool:
        pattern1 = r"^\d{4}-\d{2}-\d{2}_Kontoauszug_\d{1}_\d{4}_vom_\d{2}\.\d{2}\.\d{4}_zu_Konto_\d{10}\.pdf$"
        pattern2 = r"^\d{4}-\d{2}-\d{2}_Kontoauszug_\d{2}_\d{4}_vom_\d{2}\.\d{2}\.\d{4}_zu_Konto_\d{10}\.pdf$"
        isP1 = re.match(pattern1, filename) is not None
        isP2 = re.match(pattern2, filename) is not None
        return isP1 or isP2

    def txt2struc(self, txt) -> Account:
        text = txt.splitlines()

        konto = None
        start = None
        end = None
        data = []

        inState = 0
        line = 0

        pattern = r"\d{2}\.\d{2}\.\d{4}"

        k_type = debitor = summary1 = summary2 = summary3 = ""

        for i in range(0, len(text)):

            if inState > 0:
                line += 1

            if not konto and "Kontoauszug" in text[i]:
                konto = text[i].split(" ")[1]

            if start and not end and "Kontostand am" in text[i]:
                saldo = text[i]
                saldo = saldo.split(" ")[-1]
                saldo = saldo.replace(".", "").replace(",", ".")
                end = round(float(saldo), 2)
                print(f"Endsaldo detected: <{text[i]}> --> <{end}>")

            if not start and "Kontostand am" in text[i]:
                saldo = text[i]
                saldo = saldo.split(" ")[-1]
                saldo = saldo.replace(".", "").replace(",", ".")
                start = round(float(saldo), 2)
                print(f"Startsaldo detected: <{text[i]}> --> <{start}>")

            if re.match(pattern, text[i]):
                inState = i
                # print(f"Pattern detected: <{text[i]}> --> <{inState}>")
                day = text[i][0:10]
                split = text[i].split("/")
                k_type = split[0][10:]

            main = MISSING
            sub = MISSING

            if inState > 0 and text[i].startswith("  "):
                # print(f"Leaving item {i} {text[i]}")
                inState = 0
                line = 0
                value = round(
                    float(text[i].strip().replace(".", "").replace(",", ".")), 2
                )
                debit = "S" if value < 0 else "H"
                if value < 0:
                    value *= -1

                texts = [summary1, summary2, summary3]

                item = AccountItem(
                    date=day,
                    pn_text=k_type,
                    debitor=debitor,
                    texts=texts,
                    main_category=main,
                    sub_category=sub,
                    value=value,
                    debit=debit,
                    pn = 0
                )
                data.append(item)

                k_type = debitor = summary1 = summary2 = summary3 = ""

            if line == 1:
                debitor = text[i]

            if line == 2:
                summary1 = text[i]

            if line == 3:
                summary2 = text[i]

            if line == 4:
                summary3 = text[i]

        return Account(
            type = self.type,
            konto=self.name,
            description = self.description,
            account=self.kontonr,
            auszug=konto,
            startSaldo=start,
            endSaldo=end,
            items=data,
        )
