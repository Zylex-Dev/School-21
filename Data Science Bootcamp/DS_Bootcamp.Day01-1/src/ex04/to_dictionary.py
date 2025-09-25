def convert_to_dict(tuples) -> dict:
    result = {}
    for country, number in tuples:
        if number not in result:
            result[number] = []
        result[number].append(country)
    return result


def main():
    list_of_tuples = [
        ("Russia", "25"),
        ("France", "132"),
        ("Germany", "132"),
        ("Spain", "178"),
        ("Italy", "162"),
        ("Portugal", "17"),
        ("Finland", "3"),
        ("Hungary", "2"),
        ("The Netherlands", "28"),
        ("The USA", "610"),
        ("The United Kingdom", "95"),
        ("China", "83"),
        ("Iran", "76"),
        ("Turkey", "65"),
        ("Belgium", "34"),
        ("Canada", "28"),
        ("Switzerland", "26"),
        ("Brazil", "25"),
        ("Austria", "14"),
        ("Israel", "12"),
    ]
    dictionary = convert_to_dict(list_of_tuples)
    for key in dictionary:
        for country in dictionary[key]:
            print(f"'{key}' : '{country}'")


if __name__ == "__main__":
    main()
