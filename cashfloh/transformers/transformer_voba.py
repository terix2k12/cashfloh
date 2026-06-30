import re
from typing import List

from cashfloh.core.settings import TransformerSettings
from cashfloh.model.account import Account
from cashfloh.model.item import AccountItem
from cashfloh.transformers.transformer import Transformer


class VobaTransformer(Transformer):

    type: str = "VobaTransformer"
    name: str
    kontonr: str
    description: str

    def __init__(self, settings: List[TransformerSettings]):
        config = list(filter(lambda p: p.type == self.type, settings))
        assert len(config) == 1
        self.kontonr = config[0].account
        self.name = config[0].name
        self.description = config[0].description

    def checkFilename(self, filename):
        pattern_1 = (
            r"^\d{9}_\d{4}_Nr\.\d{3}_Kontoauszug_vom_\d{4}\.\d{2}\.\d{2}_\d{14}\.pdf$"
        )
        pattern_2 = (
            r"^\d{9}_\d{4}_Nr\.\d{3}_Kontoauszug_vom_\d{4}\.\d{2}\.\d{2}_\d{17}\.pdf$"
        )
        return re.match(pattern_1, filename) is not None or re.match(pattern_2, filename) is not None

    def txt2struc(self, txt) -> Account:
        text = txt.splitlines()

        konto_auszug = None
        start_saldo = None
        end_saldo = None
        data = []

        for i in range(0, len(text)):

            if not konto_auszug and text[i] == str(self.kontonr):
                 konto_auszug = text[i + 1].strip()
                 continue

            if not start_saldo and text[i] == "VorgangWert":
                temp = text[i + 1].strip()
                temp = temp.split(" ")[0]
                temp = temp.replace(".", "").replace(",", ".")
                start_saldo = float(temp)
                print(f"Startsaldo detected: <{temp}> --> <{start_saldo}>")
                continue

            if not end_saldo and "neuer Kontostand vom" in text[i]:
                split1 = text[i].split(" H")[0]
                split = split1.split(" ")
                end_saldo = float(split[-1].replace(".", "").replace(",", "."))
                print(f"Endsaldo detected: <{text[i]}> --> <{end_saldo}>")
                continue

            if "PN:" in text[i]:
                split = text[i].replace("  ", " ").split(" ")
                year = konto_auszug.split("/")[1]
                day = split[0]+year
                debit = split[-1]
                pn_text = split[2]
                pn_idx = text[i].find("PN:")
                pn = int(text[i][pn_idx+3:pn_idx+6].strip())
                value = float(split[-2].replace(".", "").replace(",", "."))

                j = 2
                texts = []
                while "PN:" not in text[i+j] and pn != 905 and not "bertrag auf Blatt " in text[i+j]:
                    texts.append(text[i + j])
                    j = j + 1

                item = AccountItem(
                    date=day,
                    debitor=text[i + 1],
                    debit=debit,
                    main_category=None,
                    sub_category=None,
                    value=value,
                    texts=texts,
                    pn=pn,
                    pn_text=pn_text,
                )
                data.append(item)

        return Account(
            type=self.type,
            konto=self.name,
            description=self.description,
            account=self.kontonr,
            auszug=konto_auszug,
            startSaldo=start_saldo,
            endSaldo=end_saldo,
            items=data
        )
