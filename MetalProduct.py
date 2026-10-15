from dataclasses import dataclass, replace


@dataclass(frozen=True)
class MetalProduct:
    """Fizyczny produkt z metalu, który osoba prywatna kupi u dealera (np. w Poznaniu lub z wysyłką).

    Cena zakupu = spot × waga × (1 + marża dealera) × (1 + VAT); cena odkupu = spot × waga × (1 − dyskonto skupu).
    Osoba prywatna sprzedaje bez VAT, więc VAT zapłacony przy zakupie srebra i platyny przepada.
    """

    key: str
    metal: str                    # gold / silver / platinum
    name: str
    weight_oz: float              # czysty metal w uncjach trojańskich
    vat_pct: float                # 0 dla złota inwestycyjnego, 23 dla srebra i platyny
    dealer_premium_pct: float     # marża ponad spot przed VAT
    buyback_discount_pct: float   # o ile skup płaci mniej niż spot
    note: str = ""

    def buy_price(self, spot_per_oz: float) -> float:
        return spot_per_oz * self.weight_oz * (1 + self.dealer_premium_pct / 100) * (1 + self.vat_pct / 100)

    def sell_price(self, spot_per_oz: float) -> float:
        return spot_per_oz * self.weight_oz * (1 - self.buyback_discount_pct / 100)

    def round_trip_cost_pct(self) -> float:
        """Ile procent traci się na samym kupnie i natychmiastowej sprzedaży (spread + VAT)."""
        return 100 * (1 - self.sell_price(1.0) / self.buy_price(1.0))

    def with_changes(self, **changes) -> "MetalProduct":
        return replace(self, **changes)
