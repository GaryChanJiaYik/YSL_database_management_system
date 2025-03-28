
def convertTimeStampToId(timestamp):
    exclude = [" ", "/", ":"]
    result = ""
    for char in timestamp:
        if char not in exclude:
            result += char
    return result
    