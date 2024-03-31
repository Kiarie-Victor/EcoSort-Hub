def initials(value: str):
    """
    Function to generate initials from a given string value (presumably a name).

    Args:
    - value (str): The string value representing the name.

    Returns:
    - str: The initials of the name.

    Example:
    >>> initials('John Doe')
    'JD'
    >>> initials('Alice')
    'A'
    """
    initials = ''
    splitted_name = value.split(" ")  # Split the name into parts
    if len(splitted_name) > 1:  # If there are multiple parts (first name and last name)
        first_name = splitted_name[0]
        last_name = splitted_name[-1]
        # Take the first letter of each and make them uppercase
        initials = first_name[0].upper() + last_name[0].upper()
    else:  # If there's only one part
        # Take the first letter and make it uppercase
        initials = splitted_name[0][0].upper()

    return initials
