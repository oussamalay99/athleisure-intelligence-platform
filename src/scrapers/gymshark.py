import urllib.parse
from typing import Any
from bs4 import BeautifulSoup

from .base import BaseScraper


class GymSharkScraper(BaseScraper):
    source_name = "gymshark"

    def __init__(self, base_url: str):
        super().__init__(base_url)

    def get_total_products_number(self):
        response = self.httpClient.get(self.base_url)
        soup = BeautifulSoup(response.text, "lxml")
        total_res_element = soup.select("p.pagination_pagination-text__cC_Lu")[0]
        total_products = int(total_res_element.text.split()[-2])
        total_pages = round(total_products / 60)
        return total_products, total_pages

    # Fetching the total products from the front is not always accurate
    # Proposed solution is increment the page parameter until ther is no result
    # TODO
    def discover_product_urls_per_page(self, page: int = 0) -> list[str]:
        product_urls = []
        # try:
        #     response = self.httpClient.get(self.base_url)

        #     # print("Status:", response.status_code)
        #     # print("Content-Type:", response.headers.get("content-type"))
        #     # print("Response Length:", len(response.text))
        #     # print("First 500 chars:")
        #     # print(response.text[:5000])

        # except Exception as exc:
        #     print(
        #         f"[{self.source_name}] - Error: while getting response from {self.base_url}"
        #     )
        #     return []
        params = {"page": page}
        url = f"{self.base_url}?{urllib.parse.urlencode(params)}"
        soup = self.soup(url=url)
        if soup is None:
            return []
        products_section = soup.select_one("div.pagination_pagination__rI_ag")
        products_imgs = products_section.select("div.product-card_image-wrap__s68z6")
        print(f"page: {page+1} - Total products: {len(products_imgs)}")

        for img in products_imgs:
            product_link = img.a.get("href")
            # print(product_link)
            product_urls.append(product_link)
        # for link in product_links:
        #     print(link.get("href"))

        return product_urls

    def discover_product_urls(self):
        return super().discover_product_urls()

    # TODO
    def scrape_product(self, product_url) -> dict[str, Any]:
        return super().scrape_product(product_url)
