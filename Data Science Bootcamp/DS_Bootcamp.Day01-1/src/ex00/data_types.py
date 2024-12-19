def data_types() -> None:
    a = []
    x = 50
    a.append(type(x).__name__)
    x = "Hello World"
    a.append(type(x).__name__)
    x = 60.5
    a.append(type(x).__name__)
    x = True
    a.append(type(x).__name__)
    x = ["a", "b", "c"]
    a.append(type(x).__name__)
    x = {"name": "Ilya", "age": 20}
    a.append(type(x).__name__)
    x = ("a", "b", "c")
    a.append(type(x).__name__)
    x = {"a", "b", "c"}
    a.append(type(x).__name__)

    formatted_output = "[" + ", ".join(a) + "]"
    print(formatted_output)


if __name__ == '__main__':
    data_types()
