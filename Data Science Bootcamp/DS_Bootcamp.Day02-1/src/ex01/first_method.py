class Research:

    def file_reader(self):
        with open("data.csv", "r") as file:
            data = file.read()
            return data


if __name__ == "__main__":
    a = Research()
    try:
        print(a.file_reader())
    except FileNotFoundError:
        print("Error: file data.csv not found.")
    except PermissionError:
        print("Error: insufficient permissions to read the file data.csv.")
    except Exception as e:
        print(f"Unknown Error: {e}")
