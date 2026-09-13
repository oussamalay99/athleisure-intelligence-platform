from typing import Any

from .base import BaseScraper


class GymSharkScraper(BaseScraper):
    source_name = "gymshark"

    def __init__(self, base_url: str):
        super().__init__(base_url)

    def scrape_product(self, product_url) -> dict[str, Any]:
        return super().scrape_product(product_url)
