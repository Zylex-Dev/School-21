import sys


def caesar_cipher(text, shift, mode):
    if not all(ord(char) < 128 for char in text):
        raise ValueError("The script does not support your language yet.")

    result = []
    shift = shift if mode == "encode" else -shift

    for char in text:
        if char.isalpha():
            start = ord("A") if char.isupper() else ord("a")
            result.append(chr((ord(char) - start + shift) % 26 + start))
        else:
            result.append(char)

    return "".join(result)


def main():
    if len(sys.argv) != 4:
        raise ValueError("Incorrect number of arguments")

    mode, text, shift = sys.argv[1], sys.argv[2], sys.argv[3]

    if mode not in ("encode", "decode"):
        raise ValueError("Mode must be either 'encode' or 'decode'.")

    try:
        shift = int(shift)
    except ValueError:
        raise ValueError("Shift must be an integer.")

    try:
        result = caesar_cipher(text, shift, mode)
        print(result)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
