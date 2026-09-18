from src.scrapers.gymshark import GymSharkScraper

GS = GymSharkScraper(base_url="https://www.gymshark.com/collections/all-products/mens")

total = GS.get_total_products_number()
print(total)