import unittest
from src.scraper import get_favicon_url

class TestScraper(unittest.TestCase):
    def test_valid_url(self):
        url = "https://example.com"
        favicon_url = get_favicon_url(url)
        self.assertIsNotNone(favicon_url)

    def test_invalid_url(self):
        with self.assertRaises(ValueError):
            get_favicon_url("invalid_url")

if __name__ == "__main__":
    unittest.main()