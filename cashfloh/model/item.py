import dataclasses

from cashfloh.model.categories import MainCategory, SubCategory

EMPTY = "No description computed."

@dataclasses.dataclass
class AccountItem:
    date: str
    debitor: str
    debit: str
    value: float
    texts: list[str]
    pn: int
    pn_text: str
    description: str = EMPTY
    main_category: MainCategory | None = None
    sub_category: SubCategory | None = None

    def printItem(self, c):
        main = str(self.main_category).ljust(12, " ")
        sub = str(self.sub_category).ljust(12, " ")

        print(f" {str(c).rjust(3, " ")}: {self.date}              {main} {sub}")
        print(f"                          <{self.debit.ljust(60, ' ')}>  ")
        print(f"                          <{self.debitor.ljust(60, ' ')}>  ")
        for text in self.texts:
            print(f"                          <{text.ljust(60, ' ')}>  ")
        print(
            f"                                                     {self.value:10.2f} {self.debit}"
        )
        pass


