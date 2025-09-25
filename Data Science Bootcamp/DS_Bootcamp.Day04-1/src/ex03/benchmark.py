import timeit
import sys
from functools import reduce


def loop_sum(num: int) -> None:
    res = 0
    for i in range(1, num + 1):
        res = res + i * i


def reduce_sum(num: int) -> None:
    reduce(lambda x, y: x + y, (i * i for i in range(1, num + 1)))


def measure_time(func_name: str, number_for_calc: int, num_calls: int) -> float:
    """Measures execution time of a given function."""
    setup_code = f"from __main__ import {func_name}"
    test_code = f"{func_name}({number_for_calc})"
    return timeit.timeit(stmt=test_code, setup=setup_code, number=num_calls)


def main():
    if len(sys.argv) != 4:
        raise ValueError(
            "Needs to be provided <function> <number of calls> <number for calculation>"
        )

    func_name = sys.argv[1]
    try:
        num_of_calls = int(sys.argv[2])
        num_for_calc = int(sys.argv[3])
    except ValueError:
        print(
            "ERROR: Arguments <number of calls> and <number for calculation> needs to be int"
        )
        sys.exit(1)

    match func_name:
        case "loop":
            print(measure_time("loop_sum", num_for_calc, num_of_calls))
        case "reduce":
            print(measure_time("reduce_sum", num_for_calc, num_of_calls))
        case _:
            raise ValueError("Invalid function name. Choose: <loop> or <reduce>")


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"ERROR: {e}")
