import json
from tqdm import tqdm
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
        self.OUTPUT_FILE: str = f"data/raw/{self.source_name}/products_raw.json"

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
        print(f"[{self.source_name}] - Fetching products urls ...")
        products_urls = self.discover_product_urls()
        print(f"[{self.source_name}] - 5 first products urls:\n {products_urls[:5]}")
        print(f"[{self.source_name}] - Scraping products ...")
        products = []
        for product_url in tqdm(
            products_urls,
            desc=f"[{self.source_name}] Products",
            unit="product"
        ):
            try:
                product = self.scrape_product(product_url)

                if product:
                    products.append(product)

            except Exception as e:
                print(f"[{self.source_name}]" f"Failed: {product_url} - {e}")

        print(f"{self.source_name} saving products {self.OUTPUT_FILE}...")
        try:
            with open("data/raw/gymshark/product_urls.json", "w") as f:
                json.dump(products_urls, f, indent=4)
        except Exception as e:
            print(
                f"{self.source_name} Failed saving products in this file {self.OUTPUT_FILE}"
            )
            print(e)
        return products
