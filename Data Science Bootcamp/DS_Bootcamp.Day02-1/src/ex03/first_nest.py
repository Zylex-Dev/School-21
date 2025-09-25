import sys
import os


class Research:
    def __init__(self, file_path):
        self.path = file_path

    def file_reader(self, has_header=True) -> list:
        list_of_lists = []
        with open(self.path, "r") as file:
            lines = file.readlines()
            if has_header:
                lines = lines[1:]
            for line in lines:
                try:
                    list_of_lists.append([int(x) for x in line.strip().split(",")])
                except ValueError:
                    raise ValueError("File contains invalid data")
        return list_of_lists

    class Calculations:
        def counts(self, lists_of_data):
            heads_count = sum(row[0] for row in lists_of_data)
            tails_count = sum(row[1] for row in lists_of_data)
            return heads_count, tails_count

        def fractions(self, head_count, tails_count):
            total_amount = head_count + tails_count
            if total_amount == 0:
                raise ValueError("No data to calculate fractions")
            head_percent = head_count / total_amount * 100
            tails_percent = tails_count / total_amount * 100
            return head_percent, tails_percent


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError("One argument needs to be provided")

        path_to_file = sys.argv[1]
        if not os.path.exists(path_to_file):
            raise ValueError(f"File '{path_to_file}' does not exist")

        research = Research(path_to_file)
        data = research.file_reader()
        print(data)

        calculations = research.Calculations()
        heads, tails = calculations.counts(data)
        print(heads, tails)

        head_fraction, tails_fraction = calculations.fractions(heads, tails)
        print(head_fraction, tails_fraction)
    except Exception as e:
        print(f"An error occurred: {e}")
