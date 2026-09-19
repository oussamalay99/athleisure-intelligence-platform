from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from typing import Any
from .http_client import HttpClient


class BaseScraper(ABC):
    """
    Base Interface for all e-commerce scrapers

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    source_name: str

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.httpClient = HttpClient()

    @abstractmethod
    def discover_product_urls(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def scrape_product(self, product_url: str) -> dict[str, Any]:
        raise NotImplementedError

    def soup(self, url: str, parser: str = "lxml"):
        try:
            res = self.httpClient.get(url)
        except Exception as e:
            print(f"Error while getting resoponse from : {url}")
            return None
        soup = BeautifulSoup(res.text, parser)
        return soup

    def scrape(self) -> list[dict[str, Any]]:
        products_urls = self.discover_product_urls()

        products = []

        for product_url in products_urls:
            try:
                product = self.scrape_product(product_url)

                if product:
                    products.append(product)

            except Exception as e:
                print(f"[{self.source_name}]" f"Failed: {product_url} - {e}")

        return products
