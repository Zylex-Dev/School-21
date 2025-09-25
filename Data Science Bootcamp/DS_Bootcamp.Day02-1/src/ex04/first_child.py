import sys
from random import randint


class Research:
    def __init__(self, file_path):
        self.path = file_path

    def file_reader(self, has_header=True) -> list:
        list_of_lists = []
        try:
            with open(self.path, "r") as file:
                lines = file.readlines()
                if not lines:
                    raise ValueError("The file is empty!")
                if has_header:
                    lines = lines[1:]
                for line in lines:
                    stripped_line = line.strip()
                    if not stripped_line:
                        continue
                    split_line = stripped_line.split(",")
                    if len(split_line) != 2 or not all(item.isdigit() for item in split_line):
                        raise ValueError("File contains invalid or improperly formatted data")
                    list_of_lists.append([int(x) for x in split_line])
        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.path} does not exist")
        return list_of_lists

    class Calculations:
        def __init__(self, data):
            self.data = data

        def counts(self):
            heads_count = sum(row[0] for row in self.data)
            tails_count = sum(row[1] for row in self.data)
            return heads_count, tails_count

        def fractions(self, head_count, tails_count):
            total_amount = head_count + tails_count
            if total_amount == 0:
                raise ValueError("No data to calculate fractions")
            head_percent = head_count / total_amount * 100
            tails_percent = tails_count / total_amount * 100
            return head_percent, tails_percent


class Analytics(Research.Calculations):
    HEAD = [1, 0]
    TAIL = [0, 1]

    def __init__(self, data):
        super().__init__(data)

    def predict_random(self, number_of_predictions) -> list:
        return [self.HEAD if randint(0, 1) else self.TAIL for _ in range(number_of_predictions)]

    def predict_last(self) -> list:
        if not self.data:
            raise ValueError("No data available to predict the last observation")
        return self.data[-1]


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError("One argument needs to be provided")

        path_to_file = sys.argv[1]

        research = Research(path_to_file)
        data = research.file_reader()
        print(data)

        calculations = research.Calculations(data)
        heads, tails = calculations.counts()
        print(heads, tails)

        head_fraction, tails_fraction = calculations.fractions(heads, tails)
        print(head_fraction, tails_fraction)

        analytics = Analytics(data)
        print(analytics.predict_random(3))
        print(analytics.predict_last())

    except Exception as e:
        print(f"An error occurred: {e}")
