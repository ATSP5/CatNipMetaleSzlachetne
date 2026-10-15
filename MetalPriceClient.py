import time

import pandas as pd

from InputFileLocator import InputFileLocator
from MetalPriceHistory import MetalPriceHistory
from MetalSettings import MetalSettings


class MetalPriceClient:
    """Pobiera dzienne notowania złota, srebra i platyny w USD/oz (Yahoo Finance, kontrakty COMEX/NYMEX)
    i kurs USD/PLN, przelicza na złote za uncję.

    Kopia trafia do output/metal_prices.csv; świeższa niż price_cache_hours jest używana bez sieci,
    a starsza — gdy pobieranie się nie uda.
    """

    TICKERS = {"gold": "GC=F", "silver": "SI=F", "platinum": "PL=F", "usdpln": "PLN=X"}

    def __init__(self, settings: MetalSettings, locator: InputFileLocator):
        self.history_from = settings.history_from
        self.cache_hours = settings.price_cache_hours
        self.cache_file = locator.output_folder() / "metal_prices.csv"

    def prices(self) -> MetalPriceHistory:
        cached = self._read_cache()
        if cached is not None and time.time() - self.cache_file.stat().st_mtime < self.cache_hours * 3600:
            return self._report(MetalPriceHistory(cached, "Yahoo Finance (kopia z output/metal_prices.csv)"))
        try:
            frame = self._download()
            frame.to_csv(self.cache_file)
            return self._report(MetalPriceHistory(frame, "Yahoo Finance: GC=F, SI=F, PL=F × PLN=X"))
        except Exception as error:
            if cached is not None:
                print("[ceny] pobieranie nie powiodło się (%s) — używam zapisanej kopii." % error, flush=True)
                return self._report(MetalPriceHistory(cached, "Yahoo Finance (zapisana kopia)"))
            raise RuntimeError("Nie udało się pobrać cen metali i nie ma zapisanej kopii: %s" % error)

    def _download(self) -> pd.DataFrame:
        import yfinance as yf
        raw = yf.download(list(self.TICKERS.values()), start=self.history_from, progress=False,
                          auto_adjust=False, threads=False)["Close"]
        usd = raw.rename(columns={v: k for k, v in self.TICKERS.items()})
        usd.index = pd.to_datetime(usd.index).tz_localize(None)
        usd = usd.sort_index().ffill(limit=5).dropna()
        if len(usd) < 500:
            raise RuntimeError("za mało notowań (%d)" % len(usd))
        frame = pd.DataFrame({metal: usd[metal] * usd["usdpln"] for metal in MetalPriceHistory.METALS})
        frame["usdpln"] = usd["usdpln"]
        return frame

    def _read_cache(self):
        try:
            frame = pd.read_csv(self.cache_file, index_col=0, parse_dates=True)
            return frame if len(frame) > 500 and set(MetalPriceHistory.METALS) <= set(frame.columns) else None
        except (OSError, ValueError):
            return None

    @staticmethod
    def _report(history: MetalPriceHistory) -> MetalPriceHistory:
        print("[ceny] %s: złoto %.0f zł/oz, srebro %.2f zł/oz, platyna %.0f zł/oz (%d dni od %s) — %s"
              % (history.as_of, history.spot("gold"), history.spot("silver"), history.spot("platinum"),
                 len(history.daily), history.daily.index[0].date(), history.source), flush=True)
        return history
