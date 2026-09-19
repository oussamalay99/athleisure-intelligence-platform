import json
from src.scrapers.gymshark import GymSharkScraper

GS = GymSharkScraper(base_url="https://www.gymshark.com/collections/all-products/mens")

products_urls = GS.discover_product_urls()

with open("data/raw/gymshark/product_urls.json", "w") as f:
    json.dump(products_urls, f, indent=4)