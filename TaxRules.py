from datetime import date


class TaxRules:
    """Podatek od zysku przy sprzedaży metalu.

    physical — fizyczny metal to „rzecz ruchoma” (art. 10 ust. 1 pkt 8 lit. d ustawy o PIT): sprzedaż po upływie
               6 miesięcy, licząc od końca miesiąca zakupu, jest bez podatku; wcześniej zysk wchodzi do skali
               podatkowej (12% albo 32%). Podatek Belki (19%) fizycznego metalu NIE dotyczy.
    belka    — 19% od zysku niezależnie od czasu: tak jest opodatkowany metal „papierowy” (ETC/ETF, kontrakty);
               liczony obok, do porównania.
    Strata nie daje podatku ani zwrotu.
    """

    BELKA_PCT = 19.0
    FREE_AFTER_MONTHS = 6

    def tax(self) -> "TaxRules":
        return self

    def is_tax_free(self, bought: date, months_held: int) -> bool:
        """Czy sprzedaż `months_held` miesięcy po zakupie jest po 6 miesiącach od końca miesiąca zakupu."""
        free_from = self.add_months(date(bought.year, bought.month, 1), self.FREE_AFTER_MONTHS + 1)
        return self.add_months(bought, months_held) >= free_from

    def physical_tax(self, gain: float, bought: date, months_held: int, pit_pct: float) -> float:
        if gain <= 0 or self.is_tax_free(bought, months_held):
            return 0.0
        return gain * pit_pct / 100

    def belka_tax(self, gain: float) -> float:
        return max(gain, 0.0) * self.BELKA_PCT / 100

    def first_tax_free_month(self, bought: date) -> int:
        months = 0
        while not self.is_tax_free(bought, months):
            months += 1
        return months

    @staticmethod
    def add_months(day: date, months: int) -> date:
        index = day.year * 12 + day.month - 1 + months
        year, month = divmod(index, 12)
        month += 1
        last = [31, 29 if year % 4 == 0 and (year % 100 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30,
                31, 30, 31][month - 1]
        return date(year, month, min(day.day, last))
