from typing import Any
from bs4 import BeautifulSoup

from .base import BaseScraper


class GymSharkScraper(BaseScraper):
    source_name = "gymshark"

    def __init__(self, base_url: str):
        super().__init__(base_url)

    # TODO
    def discover_product_urls(self) -> list[str]:
        product_urls = []
        try:
            response = self.httpClient.get(self.base_url)

            print("Status:", response.status_code)
            print("Content-Type:", response.headers.get("content-type"))
            print("Response Length:", len(response.text))
            # print("First 500 chars:")
            # print(response.text[:5000])

        except Exception as exc:
            print(
                f"[{self.source_name}] - Error: while getting response from {self.base_url}"
            )
            return []

        soup = BeautifulSoup(response.text, "lxml")
        products_section = soup.select_one("div.pagination_pagination__rI_ag")
        products_imgs = products_section.select("div.product-card_image-wrap__s68z6")
        print("Total products:", len(products_imgs))

        for img in products_imgs:
            product_link = img.a.get("href")
            # print(product_link)
            product_urls.append(product_link)
        # for link in product_links:
        #     print(link.get("href"))

        return product_urls

    # TODO
    def scrape_product(self, product_url) -> dict[str, Any]:
        return super().scrape_product(product_url)
