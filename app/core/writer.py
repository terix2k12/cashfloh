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


def saveJson(json_path, data):
    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)
    print("Written JSON file")
