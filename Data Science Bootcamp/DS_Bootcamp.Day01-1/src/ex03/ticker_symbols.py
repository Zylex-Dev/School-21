import sys


def get_key(val):
    for key, value in get_companies().items():
        if val == value:
            return key


def get_companies() -> dict:
    return {
        "Apple": "aapl",
        "Microsoft": "msft",
        "Netflix": "nflx",
        "Tesla": "tsla",
        "Nokia": "nok",
    }


def get_stocks() -> dict:
    return {
        "aapl": 287.73,
        "msft": 173.79,
        "nflx": 416.90,
        "tsla": 724.88,
        "nok": 3.37,
    }


def show_company_and_stocks(ticker_symbol):
    ticker_symbol = ticker_symbol.lower()
    COMPANIES = get_companies()
    STOCKS = get_stocks()

    price = STOCKS.get(ticker_symbol)
    if price:
        company = get_key(ticker_symbol)
        print(f"{company} {price}")
    else:
        print("Unknown ticker")


if __name__ == "__main__":
    arguments = sys.argv[1:]
    if len(arguments) == 1:
        show_company_and_stocks(arguments[0])
    else:
        sys.exit(0)
