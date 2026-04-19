def reverse_string(input_string):
    """
    Reverses the input string.

    Args:
        input_string (str): The string to be reversed.

    Returns:
        str: The reversed string.
    """
    return input_string[::-1]


def main():
    # Example usage
    input_str = "Hello, World!"
    print(f"Original string: {input_str}")
    reversed_str = reverse_string(input_str)
    print(f"Reversed string: {reversed_str}")


if __name__ == "__main__":
    main()