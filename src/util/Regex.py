import re


def validate_positive_integer(string: str) -> bool:
    regex = re.compile(r"([1-9]+[0-9]*)?$")
    return regex.match(string) is not None


def validate_non_negative_integer(string: str) -> bool:
    regex = re.compile(r"(0|([1-9]+[0-9]*))?$")
    return regex.match(string) is not None


def validate_positive_float(string: str) -> bool:
    regex = re.compile(r"([1-9]+[0-9]*|0)?(\.[0-9]*)?$")
    return regex.match(string) is not None


def validate_positive_percentage(string: str) -> bool:
    regex = re.compile(r"((([1-9][0-9]?|0)?(\.[0-9]*)?)|100)$")
    return regex.match(string) is not None