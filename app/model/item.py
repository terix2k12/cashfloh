import dataclasses

from app.model.categories import MainCategory, SubCategory


@dataclasses.dataclass
class AccountItem:
    date: str
    debitor: str
    debit: str
    value: float
    texts: list[str]
    pn: int
    pn_text: str
    main_category: MainCategory | None = None
    sub_category: SubCategory | None = None

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


