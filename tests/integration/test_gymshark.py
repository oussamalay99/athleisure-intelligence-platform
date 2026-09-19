from src.scrapers.gymshark import GymSharkScraper

GS = GymSharkScraper(base_url="https://www.gymshark.com/collections/all-products/mens")

page1 = GS.discover_product_urls_per_page(page=0)
page2 = GS.discover_product_urls_per_page(page=1)

print(len(set(page1 + page2)))
print(set(page1 + page2))