#!/usr/bin/env python3

import cProfile, pstats
import sys
from bs4 import BeautifulSoup
import requests


# import time


def fetch_page(url: str, headers: dict) -> BeautifulSoup:
    """
    Fetches a web page and returns a BeautifulSoup object.
    Raises ConnectionError if the page cannot be fetched.
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ConnectionError(e)
    return BeautifulSoup(response.text, "html.parser")


def parse_financial_data(soup: BeautifulSoup, field: str) -> tuple:
    """
    Parses financial data from the provided BeautifulSoup object for a specific field.
    Raises ValueError if the field or data cannot be found.
    """
    fin_container = soup.find("section", {"class": "finContainer"})
    if not fin_container:
        raise ValueError("Failed to find 'finContainer' table")

    row_title = fin_container.find("div", {"class": "rowTitle"}, string=field)
    if not row_title:
        raise ValueError(f"Field '{field}' not found in the table")

    parent_row = row_title.parent

    data = [
        sibling.text.strip()
        for sibling in parent_row.find_next_siblings("div", {"class", "column"})
    ]

    if not data:
        raise ValueError(f"No data found for field '{field}'")

    return tuple([field] + data)


def get_financial_data(ticker: str, field: str) -> tuple:
    """
    Main function to fetch and parse financial data.
    Combines fetching the web page and parsing the financial data.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    }
    url = f"https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}"

    # time.sleep(5)

    soup = fetch_page(url, headers)
    return parse_financial_data(soup, field)


def main():
    """
    Main entry point of the script. Handles user input and output.
    """
    if len(sys.argv) != 3:
        print("Usage: ./financial.py <ticker> <field>")
        sys.exit(1)

    ticker = sys.argv[1].upper()
    field = sys.argv[2]

    try:
        financial_data = get_financial_data(ticker, field)
        print(financial_data)
        return financial_data

    except ConnectionError as e:
        print(f"Connection Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Data Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    financial_data = main()

    profiler.disable()

    try:
        with open("profiling-tottime.txt", "w", encoding="utf-8") as f:
            f.write(str(financial_data) + "\n")
            stats = pstats.Stats(profiler, stream=f)
            stats.strip_dirs().sort_stats("tottime")
            stats.print_stats()
    except Exception as e:
        print(f"Unable to save statistics to file: {e}")
