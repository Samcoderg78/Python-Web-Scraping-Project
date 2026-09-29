"""Q1: Scrape product listings from mdcomputers.in for a search term.

Usage:
    python q1_scraper.py "external harddrive"
    python q1_scraper.py "external harddrive" --format csv > products.csv
"""
import argparse
import csv
import json
import re
import sys

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mdcomputers.in/"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; product-scraper/1.0)"}
MAX_PAGES = 20  # safety limit


def fetch_page(term, page):
    """Download one page of search results and return its HTML."""
    params = {"route": "product/search", "search": term, "page": page}
    response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return response.text


def find_prices(link):
    """Walk up from the product link to the smallest block that contains prices."""
    box = link.parent
    while box is not None:
        if len(box.select("h3 a")) > 1:  # reached a block with several products
            return []
        prices = re.findall(r"₹\s*([\d,]+)", box.get_text())
        if prices:
            return [int(p.replace(",", "")) for p in prices]
        box = box.parent
    return []


def parse_products(html):
    """Extract name, url and prices from one results page."""
    soup = BeautifulSoup(html, "html.parser")
    products = []
    for link in soup.select("h3 a[href*='/product/']"):
        prices = find_prices(link)
        products.append({
            "name": link.get_text(strip=True),
            "url": link["href"],
            "list_price": prices[0] if len(prices) > 1 else None,  # struck-through price
            "price": prices[-1] if prices else None,               # current price
        })
    return products


def scrape(term):
    """Fetch every results page until no new products appear."""
    seen, results = set(), []
    for page in range(1, MAX_PAGES + 1):
        new = [p for p in parse_products(fetch_page(term, page)) if p["url"] not in seen]
        if not new:
            break
        seen.update(p["url"] for p in new)
        results.extend(new)
    return results


def main():
    parser = argparse.ArgumentParser(description="Scrape mdcomputers.in search results")
    parser.add_argument("term", help="search term, e.g. 'external harddrive'")
    parser.add_argument("--format", choices=["json", "csv"], default="json")
    args = parser.parse_args()

    try:
        products = scrape(args.term)
    except requests.RequestException as e:
        sys.exit(f"Request failed: {e}")

    if not products:
        sys.exit(f"No products found for '{args.term}'")

    if args.format == "json":
        print(json.dumps(products, indent=2, ensure_ascii=False))
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=products[0].keys())
        writer.writeheader()
        writer.writerows(products)


if __name__ == "__main__":
    main()
