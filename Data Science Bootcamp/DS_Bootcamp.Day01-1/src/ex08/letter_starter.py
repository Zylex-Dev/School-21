import sys


def generate_letter(email, filepath):
    name = get_name_from_email(email, filepath)
    if name:
        return f"Dear {name}, welcome to our team. We are sure that it will be a pleasure to work with you. That’s a precondition for the professionals that our company hires."


def get_name_from_email(email_address, filepath):
    try:
        with open(filepath, "r") as file:
            next(file)  # skips header
            for line in file:
                name, surname, e_mail = line.strip().split("\t")
                if e_mail == email_address:
                    return f"{name}"
        return None
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    email_to_search = sys.argv[1]
    file_path = "employees.tsv"
    result = generate_letter(email_to_search, file_path)
    if result is None:
        sys.exit(1)
    else:
        print(result)
