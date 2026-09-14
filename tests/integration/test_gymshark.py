from src.scrapers.gymshark import GymSharkScraper

GS = GymSharkScraper(base_url="https://www.gymshark.com/collections/all-products/mens")

soup = GS.discover_product_urls()
# print(type(soup))