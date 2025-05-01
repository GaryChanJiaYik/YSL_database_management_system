def checkLengthOfInput(string, minLength, maxLength):
    """
    Check if the length of the input string is within the specified range.
    
    :param string: The input string to check.
    :param minLength: The minimum length of the string.
    :param maxLength: The maximum length of the string.
    :return: True if the length is within range, False otherwise.
    """
    return minLength <= len(string) <= maxLength