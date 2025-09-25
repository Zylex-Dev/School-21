class Must_read:
    try:
        with open("data.csv", "r") as file:
            data = file.read()
            print(data)
    except FileNotFoundError:
        print(f"Error: file data.csv not found.")
    except Exception as e:
        print(f"Unknown Error: {e}")


if __name__ == "__main__":
    Must_read()
