def sort_dict_keys(dictionary) -> list:
    int_keys = [int(x) for x in dictionary]
    sorted_int_keys = sorted(int_keys, reverse=True)
    sorted_string_keys = [str(x) for x in sorted_int_keys]
    return sorted_string_keys


def convert_to_dict(tuples) -> dict:
    result = {}
    for country, number in tuples:
        # number = int(number)
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
    sorted_keys_list = sort_dict_keys(dictionary)

    for sorted_key in sorted_keys_list:
        i = 0
        for key in dictionary:
            if sorted_key == key:
                countries = dictionary.get(key)
                if len(countries) > 1:
                    for word in sorted(countries):
                        print(word)
                else:
                    print(countries[i])
                i += 1

    # sorted_items = sorted(dictionary.items(), key=lambda x: (-x[0], sorted(x[1])))
    # for _, countries in sorted_items:
    #     for country in sorted(countries):
    #         print(country)


if __name__ == "__main__":
    main()
