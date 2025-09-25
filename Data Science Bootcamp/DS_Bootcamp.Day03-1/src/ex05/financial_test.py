import pytest
from bs4 import BeautifulSoup
from financial import fetch_page, parse_financial_data, get_financial_data


# test for function 'fetch_page'
def test_fetch_page_success():
    url = "https://finance.yahoo.com/quote/AAPL/financials?p=AAPL"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    }
    soup = fetch_page(url, headers)
    assert isinstance(soup, BeautifulSoup)


def test_fetch_page_invalid_url():
    url = "https://finance.yahoo.com/invalid_url"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    }
    with pytest.raises(ConnectionError):
        fetch_page(url, headers)


def test_fetch_page_no_headers():
    url = "https://finance.yahoo.com/quote/AAPL/financials?p=AAPL"
    headers = {"": ""}

    with pytest.raises(ConnectionError):
        fetch_page(url, headers)


# tests for function 'parse_financial_data'
def test_parse_financial_data_success():
    html_content = """
    <section class="finContainer">
        <div class="column sticky yf-t22klz">
            <div class="rowTitle yf-t22klz" title="Total Revenue">Total Revenue</div>
        </div>
        <div class="column">100</div>
        <div class="column">200</div>
    </section>
    """
    soup = BeautifulSoup(html_content, "html.parser")
    result = parse_financial_data(soup, "Total Revenue")
    assert result == ("Total Revenue", "100", "200")


def test_parse_financial_data_missing_field():
    html_content = """
    <section class="finContainer">
        <div class="column sticky yf-t22klz">
            <div class="rowTitle yf-t22klz" title="Total Revenue">Total Revenue</div>
        </div>
        <div class="column">100</div>
        <div class="column">200</div>
    </section>
    """
    soup = BeautifulSoup(html_content, "html.parser")
    with pytest.raises(ValueError):
        parse_financial_data(soup, "Non-existed field")


def test_parse_financial_data_missing_ticker():
    html_content = """
        Empty HTML Content due to invalid ticker
    """
    soup = BeautifulSoup(html_content, "html.parser")
    with pytest.raises(ValueError):
        parse_financial_data(soup, "Total Revenue")


# tests for function 'get_financial_data'
def test_get_financial_data_success():
    result = get_financial_data("AAPL", "Total Revenue")
    assert isinstance(result, tuple)
    assert len(result) == 6


def test_get_financial_data_invalid_ticker():
    with pytest.raises(ValueError):
        get_financial_data("INVALID_TICKER", "Total Revenue")


def test_get_financial_data_invalid_field():
    with pytest.raises(ValueError):
        get_financial_data("AAPL", "INVALID FIELD")
