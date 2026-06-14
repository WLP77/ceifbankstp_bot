from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Start application")]
        ],
        resize_keyboard=True
    )


def yes_no_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Yes"), KeyboardButton(text="No")]
        ],
        resize_keyboard=True
    )


def skip_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Skip")]
        ],
        resize_keyboard=True
    )


def currency_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="USD"), KeyboardButton(text="EUR")],
            [KeyboardButton(text="Other")]
        ],
        resize_keyboard=True
    )


def documents_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Done"), KeyboardButton(text="Skip")]
        ],
        resize_keyboard=True
    )


def final_confirmation_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Submit application"), KeyboardButton(text="Edit")],
            [KeyboardButton(text="Cancel")]
        ],
        resize_keyboard=True
    )


def edit_field_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Company name"), KeyboardButton(text="Jurisdiction")],
            [KeyboardButton(text="Registration number"), KeyboardButton(text="Tax number")],
            [KeyboardButton(text="Contact person"), KeyboardButton(text="Position")],
            [KeyboardButton(text="Corporate email"), KeyboardButton(text="Phone number")],
            [KeyboardButton(text="Loan amount"), KeyboardButton(text="Currency")],
            [KeyboardButton(text="Desired term"), KeyboardButton(text="Purpose of financing")],
            [KeyboardButton(text="Business description"), KeyboardButton(text="Additional comments")],
            [KeyboardButton(text="Supporting documents")],
            [KeyboardButton(text="Back to summary"), KeyboardButton(text="Cancel")]
        ],
        resize_keyboard=True
    )
