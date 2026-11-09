import json
import threading
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, call

from src.scrapers.base import BaseScraper
from src.scrapers.gymshark import GymSharkScraper


class TestGymSharkDiscovery(unittest.TestCase):
    def test_discovery_stops_at_limit_and_does_not_fetch_more_pages(self):
        scraper = GymSharkScraper("https://example.com/products")
        scraper.discover_product_urls_per_page = Mock(
            side_effect=[
                ["product-1", "product-2", "product-3"],
                ["product-4", "product-5", "product-6"],
            ]
        )

        products = scraper.discover_product_urls(limit=4)

        self.assertEqual(
            products, ["product-1", "product-2", "product-3", "product-4"]
        )
        self.assertEqual(
            scraper.discover_product_urls_per_page.call_args_list,
            [call(page=0), call(page=1)],
        )

    def test_non_positive_limit_does_not_fetch_pages(self):
        scraper = GymSharkScraper("https://example.com/products")
        scraper.discover_product_urls_per_page = Mock()

        self.assertEqual(scraper.discover_product_urls(limit=0), [])
        scraper.discover_product_urls_per_page.assert_not_called()


class _ConcurrentTestScraper(BaseScraper):
    source_name = "GYMSHARK"

    def __init__(self, output_dir):
        super().__init__("https://example.com/products", output_dir=output_dir)
        self.active_workers = 0
        self.maximum_active_workers = 0
        self.lock = threading.Lock()
        self.barrier = threading.Barrier(3)

    def discover_product_urls(self, limit=120):
        return [f"product-{index}" for index in range(6)]

    def scrape_product(self, product_url):
        with self.lock:
            self.active_workers += 1
            self.maximum_active_workers = max(
                self.maximum_active_workers, self.active_workers
            )
        try:
            self.barrier.wait(timeout=2)
            return {"url": product_url}
        finally:
            with self.lock:
                self.active_workers -= 1


class TestConcurrentScraping(unittest.TestCase):
    def test_scrapes_concurrently_and_keeps_discovery_order(self):
        with tempfile.TemporaryDirectory() as output_dir:
            scraper = _ConcurrentTestScraper(output_dir)
            products = scraper.scrape(max_workers=3)
            with scraper.products_file.open(encoding="utf-8") as products_file:
                saved_products = json.load(products_file)
            with scraper.product_urls_file.open(encoding="utf-8") as urls_file:
                saved_urls = json.load(urls_file)

        self.assertEqual(
            products,
            [{"url": f"product-{index}"} for index in range(6)],
        )
        self.assertEqual(scraper.maximum_active_workers, 3)
        self.assertEqual(saved_products, products)
        self.assertEqual(saved_urls, [f"product-{index}" for index in range(6)])

    def test_rejects_non_positive_worker_count(self):
        with tempfile.TemporaryDirectory() as output_dir:
            scraper = _ConcurrentTestScraper(output_dir)

            with self.assertRaises(ValueError):
                scraper.scrape(max_workers=0)

    def test_default_output_directory_uses_source_name(self):
        scraper = GymSharkScraper("https://example.com/products")

        self.assertEqual(scraper.output_dir, Path("data") / "raw" / "gymshark")


if __name__ == "__main__":
    unittest.main()
