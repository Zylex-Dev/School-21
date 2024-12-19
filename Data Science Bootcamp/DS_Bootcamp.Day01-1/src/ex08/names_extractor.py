import sys


def process_line(input_line):
    parts = input_line.split("@", 1)
    name = parts[0].split(".")[0].title()
    surname = parts[0].split(".")[1].title()
    output_line = f"{name}\t{surname}\t{input_line}"
    return output_line


def main(path):
    try:
        with open(path, "r") as infile:
            lines = infile.readlines()
            with open("employees.tsv", "w") as outfile:
                outfile.write("Name\tSurname\tE-mail\n")
                for line in lines:
                    result_line = process_line(line)
                    outfile.write(result_line)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    path_to_file = sys.argv[1]
    main(path_to_file)
