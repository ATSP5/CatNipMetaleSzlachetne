from typing import Dict

import numpy as np
import pandas as pd

from InputFileLocator import InputFileLocator
from MetalForecast import MetalForecast
from MetalPriceHistory import MetalPriceHistory
from MetalSettings import MetalSettings


class PriceForecaster:
    """Prognozuje miesięczne ceny złota, srebra i platyny w złotych na max_forecast_months naprzód.

    Model główny: Chronos-2 (amazon/chronos-2) — wytrenowany model bazowy dla szeregów czasowych, prognozuje bez
    doszkalania i zwraca kwantyle. Zapas, gdy pakietu chronos-forecasting nie ma albo model się nie wczyta:
    bootstrap historyczny — losowanie 12-miesięcznych bloków prawdziwych miesięcznych zmian cen od 2004 r.
    Prognoza liczona jest raz, przy starcie, dla wszystkich metali naraz; strona tylko ją przycina.
    """

    QUANTILES = (0.1, 0.24, 0.5, 0.76, 0.9)
    BLOCK_MONTHS = 12

    def __init__(self, settings: MetalSettings, prices: MetalPriceHistory, locator: InputFileLocator):
        self.settings = settings
        self.prices = prices
        self.model_dir = locator.model_folder()
        self.horizon = settings.max_forecast_months
        self.problem = None
        self._forecasts: Dict[str, MetalForecast] = {}

    def forecaster(self) -> "PriceForecaster":
        self._forecasts = self._compute()
        return self

    def forecast(self, metal: str) -> MetalForecast:
        return self._forecasts[metal]

    @property
    def model_label(self) -> str:
        return next(iter(self._forecasts.values())).model if self._forecasts else "—"

    # -- liczenie -----------------------------------------------------------------------------------
    def _compute(self) -> Dict[str, MetalForecast]:
        monthly = self.prices.monthly()
        # bieżący miesiąc jest niepełny: zastępujemy go dzisiejszym spotem, żeby prognoza startowała od dziś
        history = monthly.iloc[:-1].copy()
        months = [(monthly.index[-1] + pd.DateOffset(months=m)).strftime("%Y-%m") for m in range(1, self.horizon + 1)]
        spots = {metal: self.prices.spot(metal) for metal in MetalPriceHistory.METALS}
        series = {metal: np.append(history[metal].dropna().to_numpy(dtype=float), spots[metal])
                  for metal in MetalPriceHistory.METALS}
        bands = self._chronos(series)
        model = "Chronos-2 (%s)" % self.settings.forecast_model
        if bands is None:
            bands = {metal: self._bootstrap(values) for metal, values in series.items()}
            model = "bootstrap historyczny (%d ścieżek)" % self.settings.bootstrap_paths
        result = {metal: MetalForecast(metal, model, spots[metal], months, bands[metal]) for metal in series}
        print("[prognoza] %s, %d mies.%s" % (model, self.horizon,
                                            "" if self.problem is None else " — " + self.problem), flush=True)
        return result

    def _chronos(self, series) -> "Dict[str, Dict[float, np.ndarray]] | None":
        try:
            import torch
            import chronos
        except ImportError as missing:
            self.problem = "Chronos-2 niedostępny (%s) — pakiet chronos-forecasting" % missing
            return None
        pipeline_class = getattr(chronos, "Chronos2Pipeline", None)
        if pipeline_class is None:
            self.problem = "zainstalowany moduł 'chronos' nie ma Chronos2Pipeline — potrzebny chronos-forecasting>=2.0"
            return None
        try:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print("[prognoza] ładuję %s na %s ..." % (self.settings.forecast_model, device), flush=True)
            pipeline = pipeline_class.from_pretrained(self.settings.forecast_model, device_map=device,
                                                      cache_dir=str(self.model_dir))
            metals = list(series)
            quantiles, _ = pipeline.predict_quantiles(
                [series[m].astype(np.float32) for m in metals], prediction_length=self.horizon,
                quantile_levels=list(self.QUANTILES))
        except Exception as error:                      # noqa: BLE001
            self.problem = "Chronos-2 nie zadziałał: %s" % error
            return None
        out = {}
        for i, metal in enumerate(metals):
            values = quantiles[i][0].cpu().numpy()      # (horyzont, kwantyle)
            out[metal] = {q: np.maximum(values[:, j], 0.0) for j, q in enumerate(self.QUANTILES)}
        return out

    def _bootstrap(self, values: np.ndarray) -> Dict[float, np.ndarray]:
        returns = np.diff(np.log(values))
        rng = np.random.default_rng(self.settings.seed)
        paths = self.settings.bootstrap_paths
        blocks = int(np.ceil(self.horizon / self.BLOCK_MONTHS))
        starts = rng.integers(0, len(returns) - self.BLOCK_MONTHS, size=(paths, blocks))
        offsets = np.arange(self.BLOCK_MONTHS)
        drawn = returns[(starts[:, :, None] + offsets).reshape(paths, -1)][:, :self.horizon]
        levels = values[-1] * np.exp(np.cumsum(drawn, axis=1))
        return {q: np.quantile(levels, q, axis=0) for q in self.QUANTILES}
