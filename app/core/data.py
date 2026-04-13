import dataclasses


@dataclasses.dataclass
class AccountItem:
    date: str
    debitor: str
    debit: str
    main_category: int
    sub_category: int
    value: float
    texts: list[str]
    pn: int
    pn_text: str

    def printItem(self, c):
        main = str(self.main_category).split(".")[1].ljust(12, " ")
        sub = str(self.sub_category).split(".")[1].ljust(12, " ")

        print(f" {str(c).rjust(3, " ")}: {self.date}              {main} {sub}")
        print(f"                          <{self.ktype.ljust(60, ' ')}>  ")
        print(f"                          <{self.debitor.ljust(60, ' ')}>  ")
        print(f"                          <{self.summary.ljust(60, ' ')}>  ")
        print(f"                          <{self.details.ljust(60, ' ')}>  ")
        print(f"                          <{self.short.ljust(60, ' ')}>  ")
        print(
            f"                                                     {self.value:10.2f} {self.debit}"
        )
        pass


@dataclasses.dataclass
class Account:
    type: str
    konto: str
    description: str
    account: str
    auszug: str
    startSaldo: float
    endSaldo: float
    items: list[AccountItem]
    habenSaldo: float = 0
    sollSaldo: float = 0

    def verifystruc(self):
        soll = 0
        haben = 0
        for i in self.items:
            # print(f" {i["date"]} {i["summary"]} {i["debit"]} {i["value"]} ")
            if i.debit == "S":
                soll += i.value
            else:
                haben += i.value

        is_saldo = round(self.startSaldo - soll + haben, 2)
        if is_saldo == self.endSaldo:
            print("Verified")

            self.habenSaldo = haben
            self.sollSaldo = soll

            return True
        else:
            raise RuntimeError(f"Verification failed, is {is_saldo} should be {self.endSaldo}")
            return False

    def printstruc(self):
        print("============================================")
        print(f" Kontoauszug: {self.kontoauszug} Einträge: {len(self.items)}")
        print(f" {"".ljust(90, ' ')} Startsaldo: {self.startSaldo}")
        c = 1
        for item in self.items:
            item.printItem(c)
            c += 1
        print(f" {"".ljust(90, ' ')} Endsaldo:   {self.endSaldo}")
        print("============================================")
        pass
