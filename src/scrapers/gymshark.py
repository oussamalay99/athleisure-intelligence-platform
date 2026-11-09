import urllib.parse
from typing import Any

from src.scrapers.base import BaseScraper


class GymSharkScraper(BaseScraper):
    source_name = "GYMSHARK"

    def discover_product_urls_per_page(self, page: int = 0) -> list[str]:
        url = f"{self.base_url}?{urllib.parse.urlencode({'page': page})}"
        soup = self.soup(url=url)

        if soup is None:
            return []

        if soup.select_one("div.no-results_no-results__x4Fv_"):
            return []

        products_section = soup.select_one("div.pagination_pagination__rI_ag")
        if products_section is None:
            return []
        products_imgs = products_section.select("div.product-card_image-wrap__s68z6")

        self.logger.info(
            "Listing page %d returned %d products", page + 1, len(products_imgs)
        )
        return [
            link["href"]
            for image in products_imgs
            if (link := image.find("a", href=True)) is not None
        ]

    def discover_product_urls(self, limit: int = 120):
        if limit <= 0:
            return []

        products_urls = []
        page = 0
        while len(products_urls) < limit:
            self.logger.info("Fetching listing page %d", page)
            try:
                page_products_urls = self.discover_product_urls_per_page(page=page)
            except Exception:
                self.logger.exception(
                    "Failed to get product URLs from listing page %d", page
                )
                break
            if not page_products_urls:
                self.logger.info("No products found on listing page %d; stopping", page)
                break
            products_urls.extend(page_products_urls[: limit - len(products_urls)])
            page += 1

        return products_urls

    def scrape_product(self, product_url: str) -> dict[str, Any]:
        soup = self.soup(product_url)
        if soup is None:
            self.logger.warning("Could not retrieve product page: %s", product_url)
            return {}

        title_div = soup.find("h1", class_="product-information_title__PGbQD")
        product_title = title_div.get_text(strip=True)

        product_cat_element = soup.find("span", class_="product-information_fit__twlPR")
        if product_cat_element:
            product_cat = product_cat_element.get_text(strip=True)
        else:
            product_cat = ""

        product_price_element = soup.find(
            "div", class_="product-information_price__LJWYG"
        ).div
        product_price = product_price_element.get_text(strip=True)

        product_rating_element = soup.find(
            "span", class_="reviews-summary_rating__foN9i"
        )
        if product_rating_element:
            product_rating = product_rating_element.get_text(strip=True)
        else:
            product_rating = ""

        product_reviews_num_element = soup.find(
            "p", class_="reviews-summary_total__C6Uwx"
        )
        if product_rating_element:
            product_reviews_num = product_reviews_num_element.get_text(
                strip=True
            ).split()[-2]
        else:
            product_reviews_num = ""

        product_designed_for_element = soup.find(
            "p", class_="default_designed-for-blurb_text__2UtsT"
        )
        if product_designed_for_element:
            product_designed_for = product_designed_for_element.get_text(strip=True)
        else:
            product_designed_for = ""
        return {
            "title": product_title,
            "category": product_cat,
            "price": product_price,
            "rating": product_rating,
            "reviews_num": product_reviews_num,
            "designed_for_section": product_designed_for,
        }
