"""
Scrape product listings from mdcomputers.in for multiple search terms.

Usage:
    python q1_scraper2.py "external harddrive" "gaming keyboard"
    python q1_scraper2.py "external harddrive" "gaming keyboard" --format csv > products.csv
"""

import argparse
import csv
import json
import re
import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mdcomputers.in/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; product-scraper/1.0)"
}
MAX_PAGES = 20


def fetch_page(term, page):
    """Download one page of search results."""
    params = {
        "route": "product/search",
        "search": term,
        "page": page,
    }

    response = requests.get(
        BASE_URL,
        params=params,
        headers=HEADERS,
        timeout=15,
    )
    response.raise_for_status()
    return response.text


def find_prices(link):
    """Extract prices from the product's containing HTML block."""
    box = link.parent

    while box is not None:
        if len(box.select("h3 a")) > 1:
            return []

        prices = re.findall(
            r"₹\s*([\d,]+)",
            box.get_text(" ", strip=True),
        )

        if prices:
            return [int(p.replace(",", "")) for p in prices]

        box = box.parent

    return []


def parse_products(html):
    """Extract product name, URL, list price, and current price."""
    soup = BeautifulSoup(html, "html.parser")
    products = []

    for link in soup.select("h3 a[href*='/product/']"):
        name = link.get_text(strip=True)

        if not name:
            continue

        prices = find_prices(link)

        products.append({
            "name": name,
            "url": urljoin(BASE_URL, link["href"]),
            "list_price": prices[0] if len(prices) > 1 else None,
            "price": prices[-1] if prices else None,
        })

    return products


def scrape_term(term, seen):
    """Scrape all result pages for one search term."""
    results = []

    for page in range(1, MAX_PAGES + 1):
        html = fetch_page(term, page)
        products = parse_products(html)

        new_products = [
            product
            for product in products
            if product["url"] not in seen
        ]

        if not new_products:
            break

        for product in new_products:
            product["search_term"] = term
            seen.add(product["url"])
            results.append(product)

    return results


def scrape(terms):
    """Scrape multiple terms and deduplicate across all searches."""
    seen = set()
    results = []

    for term in terms:
        print(
            f"Searching for: {term}",
            file=sys.stderr,
        )

        products = scrape_term(term, seen)
        results.extend(products)

        print(
            f"Found {len(products)} new products for '{term}'",
            file=sys.stderr,
        )

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Scrape MDComputers for multiple search terms"
    )

    parser.add_argument(
        "terms",
        nargs="+",
        help="One or more search terms, each in quotes if it contains spaces",
    )

    parser.add_argument(
        "--format",
        choices=["json", "csv"],
        default="json",
        help="Output format (default: json)",
    )

    args = parser.parse_args()

    try:
        products = scrape(args.terms)
    except requests.RequestException as exc:
        sys.exit(f"Request failed: {exc}")

    if not products:
        sys.exit("No products found for the supplied search terms.")

    if args.format == "json":
        print(json.dumps(products, indent=2, ensure_ascii=False))
    else:
        fields = [
            "search_term",
            "name",
            "url",
            "list_price",
            "price",
        ]

        writer = csv.DictWriter(sys.stdout, fieldnames=fields)
        writer.writeheader()
        writer.writerows(products)


if __name__ == "__main__":
    main()