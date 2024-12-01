import os
from dotenv import load_dotenv

# FastApi
from fastapi import HTTPException

# Only Production
load_dotenv(dotenv_path = '.env')


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


def validateToken(value: str) -> bool:
    if value == os.getenv("token"):
        return True

    raise HTTPException(status_code = 403, detail = "Access denied.")