class MetalSettings:
    """Ustawienia analizy metali: historia, horyzont prognozy, modele AI, pliki."""

    def __init__(self, history_from: str = "2004-01-01", max_forecast_months: int = 120,
                 forecast_model: str = "amazon/chronos-2",
                 scenario_model: str = "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7",
                 bootstrap_paths: int = 4000, seed: int = 2026, price_cache_hours: float = 12.0,
                 input_folder: str = "Input", model_cache: str = "models", cpi_history_from_year: int = 2004):
        if not 12 <= int(max_forecast_months) <= 240:
            raise ValueError("max_forecast_months: od 12 do 240 miesięcy")
        if int(bootstrap_paths) < 200:
            raise ValueError("bootstrap_paths: co najmniej 200 ścieżek")
        if not history_from[:4].isdigit() or int(history_from[:4]) < 2004:
            raise ValueError("history_from: data RRRR-MM-DD nie wcześniejsza niż 2004-01-01 (kurs USD/PLN)")
        self.history_from = history_from
        self.max_forecast_months = int(max_forecast_months)
        self.forecast_model = forecast_model
        self.scenario_model = scenario_model
        self.bootstrap_paths = int(bootstrap_paths)
        self.seed = int(seed)
        self.price_cache_hours = float(price_cache_hours)
        self.input_folder = input_folder
        self.model_cache = model_cache
        self.cpi_history_from_year = int(cpi_history_from_year)

    def settings(self) -> "MetalSettings":
        return self
