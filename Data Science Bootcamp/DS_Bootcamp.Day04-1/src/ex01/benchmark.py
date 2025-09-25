import timeit


def loop_approach(emails: list[str]) -> list[str]:
    """Uses loop to filter @gmail.com addresses."""
    gmails_list = []
    for item in emails:
        if item.endswith("@gmail.com"):
            gmails_list.append(item)
    return gmails_list


def list_comprehension_approach(emails: list[str]) -> list[str]:
    """Uses list comprehension to filter @gmail.com addresses."""
    return [item for item in emails if item.endswith("@gmail.com")]


def map_approach(emails: list[str]) -> list[str]:
    """Uses map to filter @gmail.com addresses."""
    gmail_emails = list(
        map(lambda email: email if email.endswith("@gmail.com") else None, emails)
    )
    return gmail_emails


def measure_time(func_name: str, emails: list[str], num_calls: int) -> float:
    """Measures execution time of a given function."""
    setup_code = f"from __main__ import {func_name}"
    test_code = f"{func_name}({emails})"
    return timeit.timeit(stmt=test_code, setup=setup_code, number=num_calls)


def main():
    NUMBER_OF_CALLS = 90_000_000
    emails = [
        "john@gmail.com",
        "james@gmail.com",
        "alice@yahoo.com",
        "anna@live.com",
        "philipp@gmail.com",
    ] * 5
    loop_time = measure_time("loop_approach", emails, NUMBER_OF_CALLS)
    list_comp_time = measure_time(
        "list_comprehension_approach", emails, NUMBER_OF_CALLS
    )
    map_time = measure_time("map_approach", emails, NUMBER_OF_CALLS)

    times_dict = {
        "loop": loop_time,
        "list comprehension": list_comp_time,
        "map": map_time,
    }

    fastest_method = min(times_dict)

    if fastest_method == "map":
        print("it is better to use a map")
    elif fastest_method == "list comprehension":
        print("it is better to use a list comprehension")
    else:
        print("it is better to use a loop")

    result = " vs ".join(map(str, sorted(times_dict.values())))
    print(result)


if __name__ == "__main__":
    main()
