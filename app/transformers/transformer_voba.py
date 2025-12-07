import re

from app.core.data import Account, AccountItem
from app.rules.categories import MISSING
from app.transformers.transformer import Transformer


class VobaTransformer(Transformer):

    name: str = "VobaTransformer"
    kontonr: str = "xxxx"  # TODO

    def checkFilename(self, filename):
        pattern = (
            r"^\d{9}_\d{4}_Nr\.\d{3}_Kontoauszug_vom_\d{4}\.\d{2}\.\d{2}_\d{14}\.pdf$"
        )
        return re.match(pattern, filename) is not None

    def txt2struc(self, txt) -> Account:
        text = txt.splitlines()

        konto = None
        start = None
        end = None
        data = []

        for i in range(0, len(text)):

            if not konto and text[i] == self.kontonr:
                konto = text[i + 1]

            if not start and text[i] == "VorgangWert":
                saldo = text[i + 1].strip()
                # print(f"Startsaldo detected: {saldo}")
                saldo = saldo.split(" ")[0]
                saldo = saldo.replace(".", "").replace(",", ".")
                start = float(saldo)
                print(f"Startsaldo detected: <{saldo}> --> <{start}>")

            if not end and "neuer Kontostand vom" in text[i]:
                split1 = text[i].split(" H")[0]
                split = split1.split(" ")
                end = float(split[-1].replace(".", "").replace(",", "."))
                print(f"Endsaldo detected: <{text[i]}> --> <{end}>")

            if "PN:" in text[i]:
                split = text[i].replace("  ", " ").split(" ")
                day = split[0]
                debit = split[-1]
                k_type = split[2:-3]

                debitor = text[i + 1]
                summary = text[i + 2]

                value = float(split[-2].replace(".", "").replace(",", "."))

                main = MISSING
                sub = MISSING

                item = AccountItem(
                    day, k_type, debitor, summary, main, sub, value, debit, summary
                )
                data.append(item)

        return Account("Voba Konto", konto, start, end, data) # TODO inject
