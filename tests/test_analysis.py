import unittest
from app.services.analysis import analyse, parse_number
from app.services.search import build_finn_url, parse_results

class AppTests(unittest.TestCase):
    def test_parse_number(self): self.assertEqual(parse_number("399 000 kr"), 399000)
    def test_median(self): self.assertEqual(analyse({"price": 300000}, [{"price": 400000}, {"price": 500000}, {"price": 450000}])["market_price"], 450000)
    def test_filter_and_deduplicate(self):
        car={"make":"Volvo","model":"XC60","year":2020}; items=[{"title":"Volvo XC60 2020 399 000 kr","description":"pen","url":"https://www.finn.no/mobility/item/123"},{"title":"Volvo XC60 2020 399 000 kr","description":"duplikat","url":"https://www.finn.no/mobility/item/123"},{"title":"Volvo XC90 2020 500 000 kr","description":"feil","url":"https://www.finn.no/mobility/item/456"}]
        self.assertEqual(len(parse_results(items,car)),1)
    def test_finn_url(self): self.assertIn("year_from=2018",build_finn_url({"make":"Volvo","model":"XC60","year":"2020"}))

if __name__ == "__main__": unittest.main()


