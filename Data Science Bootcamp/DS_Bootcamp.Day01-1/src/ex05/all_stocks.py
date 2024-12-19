import sys


def main(input_string):
    COMPANIES = {
        "Apple": "Aapl",
        "Microsoft": "Msft",
        "Netflix": "Nflx",
        "Tesla": "Tsla",
        "Nokia": "Nok",
    }

    STOCKS = {
        "Aapl": 287.73,
        "Msft": 173.79,
        "Nflx": 416.90,
        "Tsla": 724.88,
        "Nok": 3.37,
    }
    line = input_string.split(",")
    line = [word.strip().title() for word in line]

    for word in line:
        if word == "":
            sys.exit(0)

    for word in line:
        if word in COMPANIES:
            ticker = COMPANIES.get(word)
            print(f"{word} stock price is {STOCKS.get(ticker)}")
        elif word in STOCKS:
            company_name = [key for key, value in COMPANIES.items() if value == word]
            print(f"{word.upper()} is a ticker symbol for {company_name[0]}")
        else:
            print(f"{word} is an unknown company or an unknown ticker symbol")


if __name__ == "__main__":
    if (len(sys.argv)) == 2:
        input_string = sys.argv[1]
        main(input_string)
    else:
        sys.exit(1)
