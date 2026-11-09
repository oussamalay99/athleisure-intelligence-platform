import json
import threading
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from tqdm import tqdm

from src.scrapers.http_client import HttpClient
from src.utils.logging import get_logger


class BaseScraper(ABC):
    source_name: str

    def __init__(
        self, base_url: str, output_dir: str | Path | None = None
    ) -> None:
        self.base_url = base_url
        self.output_dir = (
            Path(output_dir)
            if output_dir is not None
            else Path("data") / "raw" / self.source_name.lower()
        )
        self.product_urls_file = self.output_dir / "product_urls.json"
        self.products_file = self.output_dir / "products.json"
        self.logger = get_logger(f"{__name__}.{self.source_name.lower()}")

        self.http_client = HttpClient()
        self._http_clients = threading.local()
        self._http_clients.client = self.http_client

    @abstractmethod
    def discover_product_urls(self, limit: int = 120) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def scrape_product(self, product_url: str) -> dict[str, Any]:
        raise NotImplementedError

    def _get_http_client(self) -> HttpClient:
        client = getattr(self._http_clients, "client", None)
        if client is None:
            client = HttpClient()
            self._http_clients.client = client
        return client

    def soup(self, url: str, parser: str = "lxml") -> BeautifulSoup | None:
        try:
            response = self._get_http_client().get(url)
        except RequestException as error:
            self.logger.warning("Request failed for %s: %s", url, error)
            return None

        return BeautifulSoup(response.text, parser)

    def scrape_product_safely(self, product_url: str) -> dict[str, Any]:
        try:
            return self.scrape_product(product_url)
        except Exception:
            self.logger.exception("Failed to scrape product: %s", product_url)
            return {}

    def _scrape_products(
        self, product_urls: list[str], max_workers: int
    ) -> list[dict[str, Any]]:
        products = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for product in tqdm(
                executor.map(self.scrape_product_safely, product_urls),
                total=len(product_urls),
                desc=f"[{self.source_name}] Products",
                unit="product",
            ):
                if product:
                    products.append(product)
        return products

    def _save_results(
        self, product_urls: list[str], products: list[dict[str, Any]]
    ) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.product_urls_file.write_text(
            json.dumps(product_urls, indent=4), encoding="utf-8"
        )
        self.products_file.write_text(
            json.dumps(products, indent=4), encoding="utf-8"
        )

    def scrape(
        self, limit: int = 120, max_workers: int = 5
    ) -> list[dict[str, Any]]:
        if max_workers < 1:
            raise ValueError("max_workers must be at least 1")

        self.logger.info("Discovering product URLs")
        product_urls = self.discover_product_urls(limit=limit)
        self.logger.info(
            "Discovered %d product URLs; first five: %s",
            len(product_urls),
            product_urls[:5],
        )

        products = self._scrape_products(product_urls, max_workers)
        self.logger.info("Saving results to %s", self.output_dir)
        self._save_results(product_urls, products)
        return products
