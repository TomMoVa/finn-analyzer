import unittest
from app.services.analysis import analyse, parse_number
from app.services.search import build_finn_url, build_query, infer_car, parse_results, valid_listing_url

class AppTests(unittest.TestCase):
    def test_parse_number(self): self.assertEqual(parse_number("399 000 kr"), 399000)
    def test_median(self): self.assertEqual(analyse({"price": 300000}, [{"price": 400000}, {"price": 500000}, {"price": 450000}])["market_price"], 450000)
    def test_filter_and_deduplicate(self):
        car={"make":"Volvo","model":"XC60","year":2020}; items=[{"title":"Volvo XC60 2020 399 000 kr","description":"pen","url":"https://www.finn.no/mobility/item/123"},{"title":"Volvo XC60 2020 399 000 kr","description":"duplikat","url":"https://www.finn.no/mobility/item/123"},{"title":"Volvo XC90 2020 500 000 kr","description":"feil","url":"https://www.finn.no/mobility/item/456"}]
        self.assertEqual(len(parse_results(items,car)),1)
    def test_finn_url(self): self.assertIn("year_from=2018",build_finn_url({"make":"Volvo","model":"XC60","year":"2020"}))
    def test_optional_query_omits_none(self): self.assertEqual(build_query({"make":"Volvo","year":None}), "site:finn.no/mobility/item Volvo")
    def test_finn_listing_url(self): self.assertEqual(valid_listing_url("https://www.finn.no/mobility/item/123"), "https://www.finn.no/mobility/item/123")
    def test_infer_car_from_indexed_title(self):
        items=[{"url":"https://www.finn.no/mobility/item/123","title":"Volvo XC60 T8 2020 til salgs","description":""}]
        self.assertEqual(infer_car(items,"https://www.finn.no/mobility/item/123"), {"make":"Volvo","model":"XC60 T8","year":2020})

if __name__ == "__main__": unittest.main()

