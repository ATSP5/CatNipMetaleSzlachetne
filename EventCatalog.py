from typing import List

from EventCategory import EventCategory


class EventCatalog:
    """Rodzaje wydarzeń i ich historyczne przykłady od 2004 r. (od kiedy jest kurs USD/PLN z Yahoo).

    Daty to dzień, w którym wiadomość dotarła do rynku; EventStudy bierze ostatnie notowanie przed nią
    jako punkt odniesienia. Lista jest ręcznie dobrana — dopisz własne wydarzenia, by poszerzyć bazę analogii.
    """

    CATEGORIES = (
        EventCategory("war", "wojna, atak zbrojny lub konflikt geopolityczny",
                      ("wojn", "atak", "inwazj", "konflikt", "zbroj", "rakiet", "bomb", "terror", "nato", "napaś",
                       "ofensyw", "izrael", "iran", "rosj", "chin", "tajwan"),
                      (("2006-07-12", "wojna Izrael–Hezbollah"), ("2014-03-01", "aneksja Krymu"),
                       ("2020-01-03", "zabicie gen. Sulejmaniego"), ("2022-02-24", "inwazja Rosji na Ukrainę"),
                       ("2023-10-07", "atak Hamasu na Izrael"), ("2024-04-13", "atak Iranu na Izrael"),
                       ("2025-06-13", "uderzenie Izraela na Iran"))),
        EventCategory("banking", "kryzys bankowy lub upadek banku, panika finansowa",
                      ("bank", "upad", "bankruct", "kryzys finans", "panik", "płynnoś", "run na"),
                      (("2007-08-09", "BNP Paribas zamraża fundusze"), ("2008-09-15", "upadek Lehman Brothers"),
                       ("2010-05-07", "kryzys zadłużenia Grecji"), ("2011-08-08", "obniżka ratingu USA"),
                       ("2023-03-10", "upadek Silicon Valley Bank"), ("2023-03-19", "przejęcie Credit Suisse"))),
        EventCategory("crash", "krach na giełdzie, recesja lub spowolnienie gospodarki",
                      ("krach", "recesj", "spowoln", "spadki na giełd", "bessa", "kryzys gospod", "bezroboc"),
                      (("2008-10-06", "krach jesienią 2008"), ("2015-08-24", "czarny poniedziałek w Chinach"),
                       ("2018-02-05", "Volmageddon"), ("2020-02-24", "COVID-19 dociera do Europy"),
                       ("2020-03-09", "krach covidowy"), ("2022-06-13", "bessa 2022"),
                       ("2025-04-03", "krach po cłach USA"))),
        EventCategory("rate_cut", "obniżka stóp procentowych lub luzowanie ilościowe przez bank centralny",
                      ("obniż", "obniżk", "luzowan", "dodruk", "qe", "tańszy pieniądz", "cięcie stóp"),
                      (("2007-09-18", "Fed tnie stopy"), ("2008-12-16", "Fed do zera"),
                       ("2010-11-03", "QE2"), ("2012-09-13", "QE3"), ("2019-07-31", "Fed tnie po raz pierwszy od 2008"),
                       ("2020-03-15", "Fed do zera, QE"), ("2024-09-18", "Fed tnie o 0,5 pp"),
                       ("2025-09-17", "Fed wznawia obniżki"))),
        EventCategory("rate_hike", "podwyżka stóp procentowych, zacieśnianie polityki pieniężnej",
                      ("podwyż", "podwyżk", "zacieśn", "jastrzęb", "drogi pieniądz", "tapering"),
                      (("2004-06-30", "Fed zaczyna podwyżki"), ("2013-05-22", "zapowiedź taperingu"),
                       ("2013-06-19", "Bernanke potwierdza tapering"), ("2015-12-16", "pierwsza podwyżka Fed od 2006"),
                       ("2022-03-16", "Fed zaczyna cykl podwyżek"), ("2022-06-15", "Fed +0,75 pp"))),
        EventCategory("inflation", "wysoka inflacja, szok cenowy, drożejąca energia",
                      ("inflacj", "drożej", "ceny rosn", "drożyzn", "ropa", "energi", "gaz"),
                      (("2008-07-16", "inflacja w USA 5%"), ("2021-05-12", "inflacja w USA 4,2%"),
                       ("2021-11-10", "inflacja w USA 6,2%"), ("2022-06-10", "inflacja w USA 8,6%"),
                       ("2022-07-13", "inflacja w USA 9,1%"))),
        EventCategory("trade_war", "cła, wojna handlowa, sankcje handlowe",
                      ("cło", "cła", "ceł", "handlow", "sankcj", "embarg", "protekcjon"),
                      (("2018-03-22", "cła USA na Chiny"), ("2018-07-06", "pierwsze cła wchodzą w życie"),
                       ("2019-05-05", "eskalacja ceł USA–Chiny"), ("2019-08-01", "nowe cła na Chiny"),
                       ("2025-02-01", "cła na Kanadę, Meksyk, Chiny"), ("2025-04-02", "„Dzień Wyzwolenia” — cła USA"))),
        EventCategory("politics", "wybory, referendum, niepewność polityczna",
                      ("wybor", "referend", "prezydent", "rząd", "polityk", "brexit", "elekcj"),
                      (("2016-06-24", "Brexit"), ("2016-11-09", "wybór D. Trumpa"), ("2019-12-13", "wybory w Wlk. Brytanii"),
                       ("2020-11-04", "wybory w USA 2020"), ("2024-11-06", "ponowny wybór D. Trumpa"))),
        EventCategory("recovery", "ożywienie gospodarcze, stymulacja, wzrost popytu przemysłowego",
                      ("ożywien", "wzrost gospod", "stymul", "popyt przemysł", "boom", "szczepion", "odbic"),
                      (("2009-03-10", "dno bessy 2009"), ("2012-07-26", "Draghi: „zrobimy wszystko”"),
                       ("2020-11-09", "szczepionka Pfizer"), ("2024-09-24", "pakiet stymulacyjny Chin"))),
        EventCategory("supply", "zakłócenie podaży metali: strajk w kopalni, awaria, sankcje na producenta",
                      ("kopal", "strajk", "górnict", "wydobyc", "podaż", "rpa", "afryk", "producent", "huta"),
                      (("2008-01-25", "przerwy w dostawach prądu w kopalniach RPA"), ("2012-08-16", "masakra w Marikanie"),
                       ("2014-01-23", "strajk w kopalniach platyny RPA"), ("2022-03-07", "sankcje na rosyjskie metale"),
                       ("2024-04-12", "zakaz rosyjskich metali na LME"))),
        EventCategory("pln_crisis", "osłabienie złotego, kryzys w Polsce, obniżka ratingu Polski",
                      ("złot", "pln", "polsk", "nbp", "rating polsk", "frank"),
                      (("2008-10-22", "złoty traci 10% w miesiąc"), ("2015-01-15", "uwolnienie kursu franka"),
                       ("2016-01-15", "S&P obniża rating Polski"), ("2020-03-12", "złoty w panice covidowej"))),
    )

    def events(self) -> "EventCatalog":
        return self

    def categories(self) -> List[EventCategory]:
        return list(self.CATEGORIES)

    def get(self, key: str) -> EventCategory:
        for category in self.CATEGORIES:
            if category.key == key:
                return category
        raise KeyError("nieznany rodzaj wydarzenia %r" % key)
