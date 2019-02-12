import unittest
import database
from database import sql_to_db
import alpha_vantage_api as av_api
import os

database.DB_PATH = os.path.join("test_data.db")
STOCK_QUOTES_TABLE = ["quote text PRIMARY KEY"]


class TestScript(unittest.TestCase):

    def setUp(self):
        self.quote = "MSFT"
        self.false_quote = "msssft"
        self.date_range = "TIME_SERIES_INTRADAY"
        self.quotes = ("MSFT", "FB")
        self.data = [
            (
                '2018-12-26 14:23:00', '98.1250', '98.1300',
                '98.0300', '98.0900', '38511'),
            (
                '2018-12-26 14:22:00', '98.2400', '98.2500',
                '98.1100', '98.1100', '52639'),
            (
                '2018-12-26 14:21:00', '98.1000', '98.2550',
                '98.0600', '98.2300', '82488')]
        self.last_entry = [
            (
                '2018-12-26 14:21:00', '98.1000', '98.2550',
                '98.0600', '98.2300', '82488')]

    def test_get_api_data(self):
        self.assertTrue(av_api.get_api_data(self.quote, self.date_range), {})

    def test_api_false_quote_error(self):
        with self.assertRaises(ValueError):
            av_api.get_api_data(self.false_quote, self.date_range)

    def test_z_api_call_limit(self):
        i = 0
        while i < 6:
            i += 1
            data = av_api.get_api_data("MSFT", "TIME_SERIES_INTRADAY")
        self.assertFalse(data, False)

    def test_set_db(self):
        data = sql_to_db("create", "stock_quotes", STOCK_QUOTES_TABLE)
        self.assertEqual(data, None)

        data = av_api.sql_to_db(
            "create",
            self.quote + "_" + "INTRADAY",
            database.QUOTE_TABLE)
        self.assertEqual(data, None)

        os.remove(database.DB_PATH)


if __name__ == '__main__':
    unittest.main()
