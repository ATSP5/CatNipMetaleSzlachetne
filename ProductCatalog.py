from typing import List

from MetalProduct import MetalProduct


class ProductCatalog:
    """Standardowe monety bulionowe i sztabki dostępne dla osoby prywatnej w Poznaniu: w punktach dealerów
    (np. Mennica Polska, Mennica Wrocławska, Tavex, Goldenmark) albo z wysyłką ubezpieczoną.

    Marże i dyskonta to typowe wartości rynkowe (orientacyjnie, październik 2026) — przed zakupem sprawdź
    cennik dealera; na stronie raportu każdą wartość można zmienić suwakiem.
    VAT: złoto inwestycyjne (sztabki ≥ 995‰, monety bulionowe ≥ 900‰) jest zwolnione; srebro i platyna — 23%.
    """

    PRODUCTS = (
        MetalProduct("gold_coin_1oz", "gold", "Złoto: moneta 1 oz (Krugerrand / Maple Leaf / Filharmonik)",
                     1.0, 0.0, 4.5, 2.5, "VAT zw.; najłatwiej sprzedać w każdym skupie"),
        MetalProduct("gold_bar_100g", "gold", "Złoto: sztabka 100 g (LBMA)", 100 / 31.1034768, 0.0, 2.5, 1.5,
                     "VAT zw.; najniższa marża na gram"),
        MetalProduct("gold_bar_10g", "gold", "Złoto: sztabka 10 g", 10 / 31.1034768, 0.0, 6.0, 3.0,
                     "VAT zw.; małe sztabki mają wyższą marżę"),
        MetalProduct("silver_coin_1oz", "silver", "Srebro: moneta 1 oz (Maple Leaf / Filharmonik)", 1.0, 23.0,
                     10.0, 10.0, "VAT 23% wliczony w cenę, nie wraca przy sprzedaży"),
        MetalProduct("silver_bar_1kg", "silver", "Srebro: sztabka 1 kg", 1000 / 31.1034768, 23.0, 5.0, 8.0,
                     "VAT 23%; niższa marża, trudniej sprzedać w całości"),
        MetalProduct("platinum_coin_1oz", "platinum", "Platyna: moneta 1 oz (Maple Leaf / Filharmonik)", 1.0, 23.0,
                     6.0, 8.0, "VAT 23%; mniej skupów niż dla złota"),
        MetalProduct("platinum_bar_1oz", "platinum", "Platyna: sztabka 1 oz", 1.0, 23.0, 5.0, 8.0,
                     "VAT 23%"),
    )
    METAL_NAMES = {"gold": "Złoto", "silver": "Srebro", "platinum": "Platyna"}

    def catalog(self) -> "ProductCatalog":
        return self

    def all(self) -> List[MetalProduct]:
        return list(self.PRODUCTS)

    def for_metal(self, metal: str) -> List[MetalProduct]:
        return [p for p in self.PRODUCTS if p.metal == metal]

    def get(self, key: str) -> MetalProduct:
        for product in self.PRODUCTS:
            if product.key == key:
                return product
        raise KeyError("nieznany produkt %r" % key)
