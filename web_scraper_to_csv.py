#!/usr/bin/env python3
"""
web_scraper_to_csv.py

A general-purpose web scraper that extracts tables and/or links from any
webpage and exports the results to CSV. Built as a freelance portfolio
demo: shows requests/BeautifulSoup usage, CLI design, and error handling.

Usage:
    python web_scraper_to_csv.py --url https://example.com --mode tables
    python web_scraper_to_csv.py --url https://example.com --mode links
    python web_scraper_to_csv.py --url https://example.com --mode both --output result.csv

Install dependencies first:
    pip install requests beautifulsoup4 --break-system-packages
"""

import argparse
import csv
import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def fetch_page(url: str) -> BeautifulSoup:
    """Fetch a URL and return a parsed BeautifulSoup object."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; PortfolioScraper/1.0)"}
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def extract_tables(soup: BeautifulSoup) -> list[list[str]]:
    """Extract all table rows from the page as a flat list of rows."""
    rows_out = []
    tables = soup.find_all("table")
    for t_index, table in enumerate(tables):
        for row in table.find_all("tr"):
            cells = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
            if cells:
                rows_out.append([f"table_{t_index}"] + cells)
    return rows_out


def extract_links(soup: BeautifulSoup, base_url: str) -> list[list[str]]:
    """Extract all links with their visible text."""
    rows_out = []
    for link in soup.find_all("a", href=True):
        text = link.get_text(strip=True) or "(no text)"
        full_url = urljoin(base_url, link["href"])
        rows_out.append([text, full_url])
    return rows_out


def write_csv(rows: list[list[str]], header: list[str], output_path: str) -> None:
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Scrape tables and/or links from a webpage into CSV.")
    parser.add_argument("--url", required=True, help="Target URL to scrape")
    parser.add_argument("--mode", choices=["tables", "links", "both"], default="both")
    parser.add_argument("--output", default="scrape_result.csv", help="Output CSV filename")
    args = parser.parse_args()

    try:
        soup = fetch_page(args.url)
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}", file=sys.stderr)
        sys.exit(1)

    if args.mode == "tables":
        rows = extract_tables(soup)
        header = ["table_id", "cell_1", "cell_2", "cell_3", "cell_4", "cell_5"]
    elif args.mode == "links":
        rows = extract_links(soup, args.url)
        header = ["link_text", "url"]
    else:
        table_rows = extract_tables(soup)
        link_rows = extract_links(soup, args.url)
        rows = [["TABLES"]] + table_rows + [["LINKS"]] + [["text", "url"]] + link_rows
        header = ["data"]

    write_csv(rows, header, args.output)
    print(f"Done. Extracted {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
