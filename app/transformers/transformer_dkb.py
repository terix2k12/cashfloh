import re

from app.rules.categories import MainCategory, SubCategory


class DkbTransformer:

    def checkFilename(self, filename) -> bool:
        pattern = r"^\d{4}-\d{2}-\d{2}_Kontoauszug_\d{1}_\d{4}_vom_\d{2}\.\d{2}\.\d{4}_zu_Konto_\d{10}\.pdf$"
        return re.match(pattern, filename) is not None

    def dkbtxt2struc(txt) -> dict:
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

            main = MainCategory.MISSING
            sub = SubCategory.MISSING

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

                item = {
                    "date": day,
                    "ktype": k_type,
                    "debitor": debitor,
                    "summary": summary1,
                    "details": summary2,
                    "main": main,
                    "sub": sub,
                    "value": value,
                    "debit": debit,
                    "short": summary3,
                }
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

        return {
            "konto": "DKB Konto",
            "kontoauszug": konto,
            "startSaldo": start,
            "endSaldo": end,
            "items": data,
        }
