import re


EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_ALLOWED_REGEX = re.compile(r"^[0-9+\-() ]+$")


def is_valid_email(value: str) -> bool:
    value = value.strip()
    return bool(EMAIL_REGEX.fullmatch(value))


def is_valid_phone(value: str) -> bool:
    value = value.strip()

    if not PHONE_ALLOWED_REGEX.fullmatch(value):
        return False

    digits_only = re.sub(r"\D", "", value)
    return 7 <= len(digits_only) <= 15


def parse_loan_amount(value: str) -> float | None:
    value = value.strip().replace(",", ".")
    value = value.replace(" ", "")

    try:
        number = float(value)
    except ValueError:
        return None

    if number <= 0:
        return None

    return number


def is_valid_desired_term(value: str) -> bool:
    value = value.strip()

    if not value:
        return False

    if len(value) > 50:
        return False

    return True
