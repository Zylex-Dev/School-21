import timeit
import sys


def loop_approach(emails: list[str]) -> list[str]:
    """Uses a loop to filter @gmail.com addresses."""
    gmails_list = []
    for item in emails:
        if item.endswith("@gmail.com"):
            gmails_list.append(item)
    return gmails_list


def list_comprehension_approach(emails: list[str]) -> list[str]:
    """Uses list comprehension to filter @gmail.com addresses."""
    return [email for email in emails if email.endswith("@gmail.com")]


def map_approach(emails: list[str]) -> list[str]:
    """Uses map to get only @gmail.com addresses."""
    gmail_emails = list(
        map(lambda email: email if email.endswith("@gmail.com") else None, emails)
    )
    return gmail_emails


def filter_approach(emails: list[str]) -> list[str]:
    """Uses filter to get only @gmail.com addresses."""
    gmail_emails = list(filter(lambda email: email.endswith("@gmail.com"), emails))
    return gmail_emails


def measure_time(func_name: str, emails: list[str], num_calls: int) -> float:
    """Measures execution time of a given function."""
    setup_code = f"from __main__ import {func_name}"
    test_code = f"{func_name}({emails})"
    return timeit.timeit(stmt=test_code, setup=setup_code, number=num_calls)


if __name__ == "__main__":
    emails = [
        "john@gmail.com",
        "james@gmail.com",
        "alice@yahoo.com",
        "anna@live.com",
        "philipp@gmail.com",
    ] * 5

    try:
        if len(sys.argv) != 3:
            raise ValueError("Needs to be provided <function> and <number of calls>")

        func_name = sys.argv[1]
        number_of_calls = int(sys.argv[2])

        match func_name:
            case "loop":
                print(measure_time("loop_approach", emails, number_of_calls))
            case "list_comprehension":
                print(
                    measure_time("list_comprehension_approach", emails, number_of_calls)
                )
            case "map":
                print(measure_time("map_approach", emails, number_of_calls))
            case "filter":
                print(measure_time("filter_approach", emails, number_of_calls))
            case _:
                raise ValueError(
                    "Invalid function name. Choose: loop, list_comprehension, map or filter"
                )

    except ValueError as e:
        print(f"Error: {e}")
