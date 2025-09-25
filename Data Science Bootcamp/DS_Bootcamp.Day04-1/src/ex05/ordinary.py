import sys
import os
import resource


def read_file(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file]

    except Exception as e:
        print(f"Error during file reading: {e}")


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError("Usage: python3 ordinary.py <rating.csv file path>")

        file = sys.argv[1]
        if not os.path.exists(file):
            raise FileNotFoundError(f"file '{file}' was not found.")

        result_list = read_file(file)

        for string in result_list:
            pass

        usage = resource.getrusage(resource.RUSAGE_SELF)
        peak_memory_gb = usage.ru_maxrss / (1024.0 * 1024.0)  # GB
        total_cpu_time_sec = usage.ru_utime + usage.ru_stime

        print(f"Peak Memory Usage = {peak_memory_gb:.3f} GB")
        print(f"User Mode Time + System Mode Time = {total_cpu_time_sec:.2f}s")

    except FileNotFoundError as f:
        print(f"FileNotFoundError: {f}")
    except Exception as e:
        print(f"ERROR: {e}")
