import argparse
import json

from pypdf import PdfReader


def pdf2text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text


def extractCategory(debitor, description):
    main = MainCategory.MISSING
    sub = SubCategory.MISSING

    return (main, sub)


def printstruc(data):
    print("============================================")
    print(f" Kontoauszug: {data.get("kontoauszug")} Einträge: {len(data.get("items"))}")
    print(f" {"".ljust(90, ' ')} Startsaldo: {data.get("startSaldo")}")
    c = 1
    for item in data["items"]:
        printItem(item, c)
        c += 1
    print(f" {"".ljust(90, ' ')} Endsaldo:   {data.get("endSaldo")}")
    print("============================================")
    pass


def printItem(item, c):
    main = str(item["main"]).split(".")[1].ljust(12, " ")
    sub = str(item["sub"]).split(".")[1].ljust(12, " ")

    print(f" {str(c).rjust(3, " ")}: {item["date"]}              {main} {sub}")
    print(f"                          <{item["ktype"].ljust(60, ' ')}>  ")
    print(f"                          <{item["debitor"].ljust(60, ' ')}>  ")
    print(f"                          <{item["summary"].ljust(60, ' ')}>  ")
    print(f"                          <{item["details"].ljust(60, ' ')}>  ")
    print(f"                          <{item["short"].ljust(60, ' ')}>  ")
    print(
        f"                                                     {item["value"]:10.2f} {item["debit"]}"
    )
    pass


def struc2csv(csv_path, data):

    headers = "Monat;Tag;Datum;Nr;Konto;Saldo;Betrag;Kategorie;Unterkategorie;Details;Sort.;Prüfsumme;\n"

    with open(csv_path, "w", newline="") as csvfile:
        csvfile.write(headers)
        c = 1
        for item in data["items"]:
            main = str(item["main"]).split(".")[1].ljust(12, " ")
            sub = str(item["sub"]).split(".")[1].ljust(12, " ")
            if main.strip() == "MISSING" or sub.strip() == "MISSING":
                main = "".ljust(12, " ")
                sub = "".ljust(12, " ")

            value = f"{item["value"]:10.2f}".replace(".", ",")

            kontoauszug = data["kontoauszug"].strip().split("/")
            auszug = f"{kontoauszug[1]}-{kontoauszug[0]}"

            pruefsumme = ""
            if c == 1:
                pruefsumme = data["startSaldo"]
            if c == len(data["items"]):
                pruefsumme = data["endSaldo"]
            if c == len(data["items"]) - 1:
                pruefsumme = data["sollSaldo"] * -1
            if c == len(data["items"]) - 2:
                pruefsumme = data["habenSaldo"]
            if pruefsumme != "":
                pruefsumme = f"{pruefsumme:10.2f}".replace(".", ",")

            saldo = "Haben" if item["debit"] == "H" else "Soll"

            csvfile.write(
                f";;{item["date"]};{auszug};{data["konto"]};{saldo};{value};{main};{sub};{str(item["debitor"]).ljust(60, ' ')};;{pruefsumme}\n"
            )
            c += 1

    print("Written CSV file")


def verifystruc(data):
    soll = 0
    haben = 0
    for i in data["items"]:
        # print(f" {i["date"]} {i["summary"]} {i["debit"]} {i["value"]} ")
        if i["debit"] == "S":
            soll += i["value"]
        else:
            haben += i["value"]

    is_saldo = round(data.get("startSaldo") - soll + haben, 2)
    if is_saldo == data.get("endSaldo"):
        print("Verified")

        data["habenSaldo"] = haben
        data["sollSaldo"] = soll

        return True
    else:
        print(f"Verification failed, is {is_saldo} should be {data.get("endSaldo")}")
        return False


def assignCategories(data):

    c = 1
    for item in data["items"]:
        (main, sub) = extractCategory(item["debitor"], item["summary"])

        if main == MainCategory.MISSING or sub == SubCategory.MISSING:
            print("Can´t assign category")
            printItem(item, c)

            for t in list(MainCategory):
                print(f" {t} {t.value} ")
            m = input("Choose main category:\n")
            main = MainCategory(int(m))
            print(f"Selected {main}")

            for t in list(SubCategory):
                print(f" {t} {t.value} ")
            m = input("Choose sub category:\n")
            sub = SubCategory(int(m))
            print(f"Selected {sub}")

        item["main"] = main
        item["sub"] = sub

        c += 1


def saveJson(json_path, data):
    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)
    print("Written JSON file")

def main(categories, rules, inputpath):

    text = pdf2text(pdf_path)
    # print(text)

    if isDkb:
        data = dkbtxt2struc(text)
    else:
        data = text2struc(text)

    ok = verifystruc(data)

    if not ok:
        printstruc(data)
    else:
        # assignCategories(data)
        saveJson(json_path, data)
        struc2csv(csv_path, data)

    pass


def parse_args():
    parser = argparse.ArgumentParser(prog="cashfloh")
    parser.add_argument("categories", type=str, nargs='+')
    parser.add_argument("rules", type=str, nargs='+')
    parser.add_argument("inputpath", type=str)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args.categories, args.rules, args.inputpath)