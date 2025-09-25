import timeit
import random
from collections import Counter


def create_dict(list_of_values: list[int]) -> dict[int, int]:
    d = {}
    for i in list_of_values:
        if i in d:
            d[i] += 1
        else:
            d[i] = 1
    return d


def create_dict_counter(list_of_values: list[int]) -> dict[int, int]:
    return dict(Counter(list_of_values))


def top_common_num(list_of_values: list[int]) -> dict[int, int]:
    d = create_dict(list_of_values)
    top_10 = dict(sorted(d.items(), key=lambda item: item[1], reverse=True)[:10])
    return top_10


def top_common_num_counter(list_of_values: list[int]) -> dict[int, int]:
    return dict(Counter(list_of_values).most_common(10))


def measure_time(func, list_of_values: list[int], num_calls: int) -> float:
    """
    Measures the execution time of the given function `func` over `num_calls`.
    Returns the average time per call.
    """
    total_time = timeit.timeit(lambda: func(list_of_values), number=num_calls)
    return total_time / num_calls


def main():
    values = [random.randint(0, 100) for _ in range(1_000_000)]
    number_of_calls = 10

    print(f"my function: {measure_time(create_dict, values, number_of_calls)}")
    print(f"Counter: {measure_time(create_dict_counter, values, number_of_calls)}")
    print(f"my top: {measure_time(top_common_num, values, number_of_calls)}")
    print(
        f"Counter`s top: {measure_time(top_common_num_counter, values, number_of_calls)}"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}")
