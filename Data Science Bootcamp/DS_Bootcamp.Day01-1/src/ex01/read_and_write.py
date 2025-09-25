def read_and_write(input_file, output_file) -> None:
    with open(input_file, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    with open(output_file, "w", encoding="utf-8") as outfile:
        for line in lines:
            result = []
            in_quotes = False
            for char in line:
                if char == '"':
                    in_quotes = not in_quotes
                if char == "," and not in_quotes:
                    result.append("\t")
                else:
                    result.append(char)
            outfile.write("".join(result))


if __name__ == "__main__":
    read_and_write("ds.csv", "ds.tsv")
