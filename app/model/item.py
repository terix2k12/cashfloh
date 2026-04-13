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
        #main = str(self.main_category).split(".")[1].ljust(12, " ")
        #sub = str(self.sub_category).split(".")[1].ljust(12, " ")
        main = self.main_category
        sub = self.sub_category

        print(f" {str(c).rjust(3, " ")}: {self.date}              {main} {sub}")
        print(f"                          <{self.debit.ljust(60, ' ')}>  ")
        print(f"                          <{self.debitor.ljust(60, ' ')}>  ")
        for text in self.texts:
            print(f"                          <{text.ljust(60, ' ')}>  ")
        # print(f"                          <{self.details.ljust(60, ' ')}>  ")
        # print(f"                          <{self.short.ljust(60, ' ')}>  ")
        print(
            f"                                                     {self.value:10.2f} {self.debit}"
        )
        pass


