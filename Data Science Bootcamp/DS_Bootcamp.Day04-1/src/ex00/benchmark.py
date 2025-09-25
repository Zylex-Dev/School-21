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
    list_comprehension_time = measure_time(
        "list_comprehension_approach", emails, NUMBER_OF_CALLS
    )

    if list_comprehension_time <= loop_time:
        print(
            f"it is better to use a list comprehension\n{list_comprehension_time} vs {loop_time}"
        )
    else:
        print(f"it is better to use a loop\n{loop_time} vs {list_comprehension_time}")


if __name__ == "__main__":
    main()
