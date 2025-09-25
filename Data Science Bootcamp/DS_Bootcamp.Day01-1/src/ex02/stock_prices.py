import sys


def get_companies():
    return {
        "apple": "AAPL",
        "microsoft": "MSFT",
        "netflix": "NFLX",
        "tesla": "TSLA",
        "nokia": "NOK",
    }


def get_stocks():
    return {
        "AAPL": 287.73,
        "MSFT": 173.79,
        "NFLX": 416.90,
        "TSLA": 724.88,
        "NOK": 3.37,
    }


def show_stock_price(company_name):
    company_name = company_name.lower()
    COMPANIES = get_companies()
    STOCKS = get_stocks()

    ticket = COMPANIES.get(company_name)
    if ticket:
        print(STOCKS.get(ticket))
    else:
        print("Unknown company")


if __name__ == "__main__":
    arguments = sys.argv[1:]
    if len(arguments) == 1:
        show_stock_price(arguments[0])
    else:
        sys.exit(0)
