import re

from app.rules.categories import MainCategory, SubCategory


class VobaTransformer:

    kontonr: str

    def checkFilename(self, filename):
        pattern = (
            r"^\d{9}_\d{4}_Nr\.\d{3}_Kontoauszug_vom_\d{4}\.\d{2}\.\d{2}_\d{14}\.pdf$"
        )
        return re.match(pattern, filename) is not None

    def text2struc(self, txt) -> dict:
        text = txt.splitlines()

        konto = None
        start = None
        end = None
        data = []

        for i in range(0, len(text)):

            if not konto and text[i] == self.kontonr:
                konto = text[i + 1]

            if not start and text[i] == "VorgangWert":
                saldo = text[i + 1]
                # print(f"Startsaldo detected: {saldo}")
                saldo = saldo.split(" ")[1]
                saldo = saldo.replace(".", "").replace(",", ".")
                start = float(saldo)
                print(f"Startsaldo detected: <{saldo}> --> <{start}>")

            if not end and "neuer Kontostand vom" in text[i]:
                split = text[i].split(" ")
                end = float(split[-2].replace(".", "").replace(",", "."))
                print(f"Endsaldo detected: <{text[i]}> --> <{end}>")

            if "PN:" in text[i]:
                split = text[i].replace("  ", " ").split(" ")
                day = split[0]
                debit = split[-1]
                k_type = split[2:-3]

                debitor = text[i + 1]
                summary = text[i + 2]

                value = float(split[-2].replace(".", "").replace(",", "."))

                main = MainCategory.MISSING
                sub = SubCategory.MISSING

                item = {
                    "date": day,
                    "ktype": k_type,
                    "debitor": debitor,
                    "summary": summary,
                    "main": main,
                    "sub": sub,
                    "value": value,
                    "debit": debit,
                    "short": summary,
                }
                data.append(item)

        return {
            "kontoauszug": konto,
            "startSaldo": start,
            "endSaldo": end,
            "items": data,
        }
