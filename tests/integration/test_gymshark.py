import json
from src.scrapers.gymshark import GymSharkScraper

GS = GymSharkScraper(base_url="https://www.gymshark.com/collections/all-products/mens")

# products_urls = GS.discover_product_urls()

# with open("data/raw/gymshark/product_urls.json", "w") as f:
#     json.dump(products_urls, f, indent=4)

# product = GS.scrape_product(
#     product_url="https://www.gymshark.com/products/gymshark-power-t-shirt-ss-tops-black-aw25-4"
# )
# urls = [
#     "https://www.gymshark.com/products/gymshark-power-t-shirt-ss-tops-black-aw25-4",
#     "https://www.gymshark.com/products/gymshark-power-t-shirt-ss-tops-black-aw25-3",
#     "https://www.gymshark.com/products/gymshark-cotton-seamless-t-shirt-ss-tops-black-aw26",
#     "https://www.gymshark.com/products/gymshark-train-t-shirt-ss-tops-black-aw26",
#     "https://www.gymshark.com/products/gymshark-global-lifting-wide-leg-pants-pants-black-aw26",
# ]

# for url in urls:
#     prod = GS.scrape_product(product_url=url)
#     print(prod)
# product = GS.scrape_product(
#     product_url="https://www.gymshark.com/products/gymshark-essentials-duffle-bag-bags-pink-aw26"
# )
# print(product)
# print(GS.OUTPUT_FILE)
GS.scrape()
