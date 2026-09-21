import urllib.parse
from typing import Any

from .base import BaseScraper


class GymSharkScraper(BaseScraper):
    source_name = "GYMSHARK"

    def __init__(self, base_url: str):
        super().__init__(base_url)

    def get_total_products_number(self):
        soup = self.soup(url=self.base_url)
        total_res_element = soup.select("p.pagination_pagination-text__cC_Lu")[0]
        total_products = int(total_res_element.text.split()[-2])
        total_pages = round(total_products / 60)
        return total_products, total_pages

    # Fetching the total products from the front is not always accurate
    # Proposed solution is increment the page parameter until ther is no result
    # TODO
    def discover_product_urls_per_page(self, page: int = 0) -> list[str]:
        product_urls = []
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

    def check_no_results_per_page(self, page: int):
        params = {"page": page}
        url = f"{self.base_url}?{urllib.parse.urlencode(params)}"
        soup = self.soup(url=url)

        if soup is None:
            return True

        no_result_section = soup.select_one("div.no-results_no-results__x4Fv_")
        if no_result_section:
            return True

        return False

    def discover_product_urls(self):
        products_urls = []
        _, max_pages = self.get_total_products_number()
        for page in range(max_pages):
            print(f"{self.source_name} - Fetching products urls for page - {page}")
            if self.check_no_results_per_page(page=page):
                print(
                    f"{self.source_name} - page: {page} : Reached the end of products"
                )
                break
            try:
                page_products_urls = self.discover_product_urls_per_page(page=page)
            except Exception as e:
                print(
                    f"{self.source_name} - Error while getting product urls for page {page}: ",
                    e,
                )
                continue
            products_urls += page_products_urls

        return products_urls

    # TODO
    def scrape_product(self, product_url) -> dict[str, Any]:
        # return super().scrape_product(product_url)
        soup = self.soup(product_url)
        if soup is None:
            print(f"{self.source_name} - Error while scraping product: {product_url}")
            return dict()

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
        # product_desc_element = soup.find()
        return {
            "title": product_title,
            "category": product_cat,
            "price": product_price,
            "rating": product_rating,
            "reviews_num": product_reviews_num,
            "designed_for_section": product_designed_for,
        }
