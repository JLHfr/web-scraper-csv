# Web Scraper to CSV

A Python CLI tool that extracts tables and/or links from any webpage and exports the results to CSV. Built for quick, reliable data collection — no browser automation needed for static pages.

## Use cases
- Competitor price monitoring
- Lead list building from directory pages
- Pulling structured data (tables) from public reports or listings
- Collecting all links from a page for further processing

## Installation

```bash
git clone https://github.com/JLHfr/web-scraper-csv.git
cd web-scraper-csv
pip install requests beautifulsoup4 --break-system-packages
```

## Usage

```bash
# Extract tables only
python web_scraper_to_csv.py --url https://example.com --mode tables

# Extract links only
python web_scraper_to_csv.py --url https://example.com --mode links

# Extract both, with a custom output filename
python web_scraper_to_csv.py --url https://example.com --mode both --output result.csv
```

## Arguments

| Argument | Required | Description |
|---|---|---|
| `--url` | Yes | The webpage to scrape |
| `--mode` | No | `tables`, `links`, or `both` (default: `both`) |
| `--output` | No | Output CSV filename (default: `scrape_result.csv`) |

## Notes
- Works on static HTML pages. Pages that render content via JavaScript will need a browser-based scraper (e.g. Selenium/Playwright) instead — happy to build that variant on request.
- Includes basic error handling for failed requests and invalid URLs.

## License
MIT — free to use and modify.

## Available for freelance work
I build custom automation and scraping tools tailored to your specific data needs. Reach out on Upwork or open an issue here to discuss a project.
