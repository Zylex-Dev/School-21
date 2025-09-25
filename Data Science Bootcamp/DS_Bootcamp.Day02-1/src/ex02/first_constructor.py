import sys
import os


class Research:
    def __init__(self, file_path):
        self.path = file_path

    def file_reader(self):
        with open(self.path, "r") as file:
            lines = file.readlines()
            if not lines:
                raise ValueError("The file is Empty!")
            return lines


def validate_data(data):
    lines = []
    for line in data:
        lines.append(line.strip())

    if len(lines) < 2 or "," not in lines[0]:
        raise ValueError("Invalid file format: Missing of incorrect header")
    header = lines[0].split(",")
    if len(header) != 2:
        raise ValueError("Invalid header format")

    for line in lines[1:]:
        if line not in {"0,1", "1,0"}:
            raise ValueError(f"Invalid data row format: {line}")
    return lines


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("One argument needs to be provided")

    path_to_file = sys.argv[1]
    research = Research(path_to_file)
    try:
        file_data = research.file_reader()

        print("\n".join(validate_data(file_data)))

    except FileNotFoundError:
        print(f"File {path_to_file} was not found")
    except ValueError as e:
        print(f"Validation Error: {e}")
