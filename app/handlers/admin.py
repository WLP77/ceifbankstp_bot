from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.config import ADMIN_CHAT_ID
from app.database import (
    ALLOWED_STATUSES,
    get_recent_applications,
    get_application_by_id,
    get_files_by_application_id,
    get_applications_by_status,
    update_application_status,
)

router = Router()


def is_admin_chat(message: Message) -> bool:
    return ADMIN_CHAT_ID is not None and message.chat.id == ADMIN_CHAT_ID


@router.message(Command("applications"))
async def cmd_applications(message: Message) -> None:
    if not is_admin_chat(message):
        return

    applications = get_recent_applications(limit=10)

    if not applications:
        await message.answer("No applications found.")
        return

    lines = ["RECENT APPLICATIONS\n"]
    for item in applications:
        lines.append(
            f"ID: {item['id']} | "
            f"Company: {item['company_name']} | "
            f"Contact: {item['contact_person']} | "
            f"Amount: {item['loan_amount']} {item['currency']} | "
            f"Status: {item['status']} | "
            f"Created: {item['created_at']}"
        )

    await message.answer("\n".join(lines))


@router.message(Command("application"))
async def cmd_application(message: Message) -> None:
    if not is_admin_chat(message):
        return

    text = (message.text or "").strip()
    parts = text.split()

    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Usage: /application <id>")
        return

    application_id = int(parts[1])
    application = get_application_by_id(application_id)

    if not application:
        await message.answer(f"Application with ID {application_id} not found.")
        return

    response = (
        "APPLICATION DETAILS\n\n"
        f"Application ID: {application['id']}\n"
        f"Created at: {application['created_at']}\n"
        f"Status: {application['status']}\n"
        f"Telegram user ID: {application['telegram_user_id']}\n"
        f"Company name: {application['company_name']}\n"
        f"Jurisdiction: {application['jurisdiction']}\n"
        f"Registration number: {application['registration_number']}\n"
        f"Tax number: {application['tax_number']}\n"
        f"Contact person: {application['contact_person']}\n"
        f"Position: {application['position']}\n"
        f"Corporate email: {application['corporate_email']}\n"
        f"Phone number: {application['phone_number']}\n"
        f"Loan amount: {application['loan_amount']}\n"
        f"Currency: {application['currency']}\n"
        f"Desired term: {application['desired_term']}\n"
        f"Purpose of financing: {application['purpose_of_financing']}\n"
        f"Business description: {application['business_description']}\n"
        f"Additional comments: {application['additional_comments']}\n"
        f"Personal data consent: {'Yes' if application['personal_data_consent'] else 'No'}\n"
        f"NCND consent: {'Yes' if application['ncnd_consent'] else 'No'}"
    )

    await message.answer(response)


@router.message(Command("files"))
async def cmd_files(message: Message) -> None:
    if not is_admin_chat(message):
        return

    text = (message.text or "").strip()
    parts = text.split()

    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Usage: /files <application_id>")
        return

    application_id = int(parts[1])
    files = get_files_by_application_id(application_id)

    if not files:
        await message.answer(f"No files found for application ID {application_id}.")
        return

    lines = [f"FILES FOR APPLICATION {application_id}\n"]
    for item in files:
        lines.append(
            f"File ID: {item['id']} | "
            f"Name: {item['file_name'] or 'Unnamed file'} | "
            f"Telegram file_id: {item['telegram_file_id']}"
        )

    await message.answer("\n".join(lines))


@router.message(Command("setstatus"))
async def cmd_setstatus(message: Message) -> None:
    if not is_admin_chat(message):
        return

    text = (message.text or "").strip()
    parts = text.split()

    if len(parts) != 3 or not parts[1].isdigit():
        await message.answer(
            "Usage: /setstatus <application_id> <status>\n\n"
            "Available statuses:\n"
            "- new\n"
            "- in_review\n"
            "- contacted\n"
            "- rejected\n"
            "- approved_next_step"
        )
        return

    application_id = int(parts[1])
    status = parts[2].strip().lower()

    if status not in ALLOWED_STATUSES:
        await message.answer(
            "Invalid status.\n\n"
            "Available statuses:\n"
            "- new\n"
            "- in_review\n"
            "- contacted\n"
            "- rejected\n"
            "- approved_next_step"
        )
        return

    updated = update_application_status(application_id, status)

    if not updated:
        await message.answer(f"Application with ID {application_id} not found.")
        return

    await message.answer(
        f"Status for application {application_id} updated to: {status}"
    )


@router.message(Command("bystatus"))
async def cmd_bystatus(message: Message) -> None:
    if not is_admin_chat(message):
        return

    text = (message.text or "").strip()
    parts = text.split()

    if len(parts) != 2:
        await message.answer(
            "Usage: /bystatus <status>\n\n"
            "Available statuses:\n"
            "- new\n"
            "- in_review\n"
            "- contacted\n"
            "- rejected\n"
            "- approved_next_step"
        )
        return

    status = parts[1].strip().lower()

    if status not in ALLOWED_STATUSES:
        await message.answer(
            "Invalid status.\n\n"
            "Available statuses:\n"
            "- new\n"
            "- in_review\n"
            "- contacted\n"
            "- rejected\n"
            "- approved_next_step"
        )
        return

    applications = get_applications_by_status(status)

    if not applications:
        await message.answer(f"No applications found with status '{status}'.")
        return

    lines = [f"APPLICATIONS WITH STATUS: {status}\n"]
    for item in applications:
        lines.append(
            f"ID: {item['id']} | "
            f"Company: {item['company_name']} | "
            f"Contact: {item['contact_person']} | "
            f"Amount: {item['loan_amount']} {item['currency']} | "
            f"Status: {item['status']} | "
            f"Created: {item['created_at']}"
        )

    await message.answer("\n".join(lines))

