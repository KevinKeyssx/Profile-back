def isString(value: str) -> bool:
    first   = value[0]
    last    = value[-1]

    if first == '[' and last == ']':
        first   = value[1]
        last    = value[2]

    if first == '"' and last == '"':
        return True

    return False

def stringToJson(value: str) -> str:
    first   = value[0]
    last    = value[-1]

    if first == '[' and last == ']':
        return value

    return '"' + value + '"'