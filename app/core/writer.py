import dataclasses
import json

from app.core.data import Account


def struc2csv(csv_path, data: Account):

    headers = "Monat;Tag;Datum;Nr;Konto;Saldo;Betrag;Kategorie;Unterkategorie;Details;Sort.;Prüfsumme;\n"

    with open(csv_path, "w", newline="") as csvfile:
        csvfile.write(headers)
        c = 1
        for item in data.items:
            main = str(item.main).ljust(12, " ")
            sub = str(item.sub).ljust(12, " ")
            if main.strip() == "MISSING" or sub.strip() == "MISSING":
                main = "".ljust(12, " ")
                sub = "".ljust(12, " ")

            value = f"{item.value:10.2f}".replace(".", ",").strip()

            if data.kontoauszug:
                kontoauszug = data.kontoauszug.strip().split("/")
                auszug = f"{kontoauszug[1]}-{kontoauszug[0]}"
            else:
                kontoauszug = "kontoauszug"
                auszug = "auszug"

            pruefsumme = ""
            if c == 1:
                pruefsumme = data.startSaldo
            if c == len(data.items):
                pruefsumme = data.endSaldo
            if c == len(data.items) - 1:
                pruefsumme = data.sollSaldo * -1
            if c == len(data.items) - 2:
                pruefsumme = data.habenSaldo
            if pruefsumme != "":
                pruefsumme = f"{pruefsumme:10.2f}".replace(".", ",").strip()
                # TODO , vs . make locale configurable

            saldo = "Haben" if item.debit == "H" else "Soll"
            debitor = str(item.debitor).ljust(60, ' ')
            details = str(item.details).ljust(60, ' ')
            sort = f"{auszug}-{str(c)}"

            csvfile.write(
                f";;{item.date};{auszug};{data.konto};{saldo};{value};{main};{sub};{details};{sort};{pruefsumme}\n"
            )
            c += 1

    print("Written CSV file")


def saveJson(json_path, data: Account):
    with open(json_path, "w") as f:
        json.dump(dataclasses.asdict(data), f, indent=4)
    print("Written JSON file")
