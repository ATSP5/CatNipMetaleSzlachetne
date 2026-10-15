from MetalSettings import MetalSettings
from ProductCatalog import ProductCatalog
from TaxRules import TaxRules
from EventCatalog import EventCatalog
from InputFileLocator import InputFileLocator
from InvestmentCalculator import InvestmentCalculator
from MetalPriceClient import MetalPriceClient
from GusInflationClient import GusInflationClient
from ScenarioClassifier import ScenarioClassifier
from PriceForecaster import PriceForecaster
from EventStudy import EventStudy
from ScenarioAnalyzer import ScenarioAnalyzer
from MetalAnalyzer import MetalAnalyzer
from MetalsPage import MetalsPage

def main():
	settings = MetalSettings()
	catalog_1 = ProductCatalog()
	tax = TaxRules()
	catalog_2 = EventCatalog()

	data_1 = settings.settings()
	data_2 = catalog_1.catalog()
	data_3 = tax.tax()
	data_4 = catalog_2.events()
	locator = InputFileLocator(data_1)
	data_5 = locator.locator()
	calculator = InvestmentCalculator(data_2, data_3)
	data_6 = calculator.calculator()
	prices = MetalPriceClient(data_1, data_5)
	data_7 = prices.prices()
	inflation = GusInflationClient(data_1, data_5)
	data_8 = inflation.inflation()
	classifier = ScenarioClassifier(data_1, data_4, data_5)
	data_9 = classifier.classifier()
	forecaster = PriceForecaster(data_1, data_7, data_5)
	data_10 = forecaster.forecaster()
	event_study = EventStudy(data_7, data_4)
	data_11 = event_study.event_study()
	scenario = ScenarioAnalyzer(data_9, data_11)
	data_12 = scenario.scenario()
	analyzer = MetalAnalyzer(data_7, data_8, data_6, data_10, data_12)
	data_13 = analyzer.analyzer()
	page = MetalsPage(data_13)
	page.show()
	pass

if __name__ == "__main__":
	main()
