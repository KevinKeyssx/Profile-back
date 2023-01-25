from utils import constants

def not_found_message(model: str):
    return constants.NOT_FOUND.replace("++", model)


def exist_message(model: str):
    return constants.EXISTS.replace("++", model)