
import json
import time
from urllib import robotparser
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com/"
MAX_PAGES = 2
OUTPUT_FILE = "quotes.json"

HEADERS = {
    "User-Agent": "StudentQuoteScraper/1.0 (educational project)"
}


def check_robots(url):
    """Check whether robots.txt permits fetching the URL."""
    robots_url = urljoin(url, "/robots.txt")
    parser = robotparser.RobotFileParser()
    parser.set_url(robots_url)

    try:
        response = requests.get(
            robots_url, headers=HEADERS, timeout=10
        )
        response.raise_for_status()
        parser.parse(response.text.splitlines())
        return parser.can_fetch(HEADERS["User-Agent"], url)
    except requests.RequestException as error:
        print(f"Could not check robots.txt: {error}")
        return False


def fetch_page(url):
    """Fetch one page and return its HTML."""
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")
    if "text/html" not in content_type.lower():
        raise ValueError("The response is not an HTML page.")

    return response.text


def extract_quotes(html, page_url):
    """Extract quotes, authors, and tags from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    records = []

    # Keep selectors together so they are easy to update.
    for item in soup.select("div.quote"):
        quote_tag = item.select_one("span.text")
        author_tag = item.select_one("small.author")

        # Skip incomplete records instead of crashing.
        if quote_tag is None or author_tag is None:
            continue

        records.append({
            "quote": quote_tag.get_text(" ", strip=True),
            "author": author_tag.get_text(" ", strip=True),
            "tags": [
                tag.get_text(" ", strip=True)
                for tag in item.select("a.tag")
            ],
            "source_url": page_url
        })

    return records


def save_json(records):
    """Save extracted records as readable JSON."""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=2, ensure_ascii=False)


def main():
    records = []
    session = requests.Session()
    session.headers.update(HEADERS)

    # Check crawling rules before fetching the first page.
    if not check_robots(BASE_URL):
        print("Cannot confirm permission to scrape. Stopping.")
        return

    for page_number in range(1, MAX_PAGES + 1):
        url = urljoin(BASE_URL, f"page/{page_number}/")

        if not check_robots(url):
            print(f"Robots rules disallow or cannot confirm: {url}")
            break

        try:
            print(f"Fetching page {page_number}...")
            html = fetch_page(url)
            page_records = extract_quotes(html, url)

            if not page_records:
                print("No quotes found. Stopping.")
                break

            records.extend(page_records)

        except (requests.RequestException, ValueError) as error:
            print(f"Request or response error: {error}")
            break

        if page_number < MAX_PAGES:
            time.sleep(2)

    session.close()
    save_json(records)
    print(f"Saved {len(records)} quotes to {OUTPUT_FILE}.")


if __name__ == "__main__":
    main()
