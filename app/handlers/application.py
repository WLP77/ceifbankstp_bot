from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from app.database import save_application
from app.config import ADMIN_CHAT_ID

from app.utils.validators import (
    is_valid_email,
    is_valid_phone,
    parse_loan_amount,
    is_valid_desired_term,
)

from app.keyboards.application import (
    yes_no_keyboard,
    skip_keyboard,
    currency_keyboard,
    documents_keyboard,
    final_confirmation_keyboard,
    edit_field_keyboard,
    main_menu_keyboard,
)
from app.states.application import ApplicationForm

router = Router()

COMPANY_DETAILS = (
    "Country of registration: Democratic Republic of São Tomé and Príncipe\n"
    "State registration number: 100725/20240517\n"
    "Tax number (N.I.F.): 517005886\n"
    "Registration date: 17.05.2024"
)

PERSONAL_DATA_CONSENT_TEXT = (
    "PERSONAL DATA PROCESSING CONSENT\n\n"
    "By selecting 'Yes', you, acting on behalf of the applicant company, confirm and agree to the following:\n\n"
    "1. You voluntarily provide personal data contained in this application, including the name of the contact person, "
    "position, corporate email address, phone number, and any personal data that may be contained in attached documents.\n\n"
    "2. You confirm that you have the right and authority to submit such information on behalf of the applicant company "
    "for the purpose of preliminary review of a credit application.\n\n"
    "3. You consent to the collection, recording, systematization, storage, clarification, use, transfer to authorized officers, "
    "and other processing operations necessary for the preliminary review of the application, follow-up communication, "
    "internal assessment, compliance procedures, and preparation of further documentation.\n\n"
    "4. Personal data may be processed both manually and by automated means.\n\n"
    "5. The submitted data will be used solely for handling the application, communication with the applicant, "
    "internal review, compliance checks, and related business correspondence.\n\n"
    "6. Submission of this application through the bot does not constitute a final banking decision, approval of financing, "
    "or conclusion of a contract.\n\n"
    "7. Consent remains valid for the period reasonably necessary to review the application and maintain related internal records, "
    "unless a different retention period is required by applicable law or internal compliance procedures.\n\n"
    "8. By selecting 'Yes', you confirm that you have read, understood, and accepted this personal data processing consent.\n\n"
    f"Company details:\n{COMPANY_DETAILS}"
)

NCND_TEXT = (
    "NON-CIRCUMVENTION AND NON-DISCLOSURE ACKNOWLEDGEMENT (NCND)\n\n"
    "By selecting 'Yes', you, acting on behalf of the applicant company, acknowledge and agree to the following:\n\n"
    "1. All non-public information disclosed through this application, including business information, financing needs, "
    "contact details, supporting documents, and transaction-related information, shall be treated as confidential.\n\n"
    "2. Such information may be used solely for the purpose of preliminary review of the proposed credit request "
    "and related communication between the parties.\n\n"
    "3. The submitting party agrees not to use this communication channel to bypass, circumvent, or improperly exclude "
    "the receiving company or its representatives from potential financing discussions, negotiations, introductions, "
    "or other related business opportunities arising from this application.\n\n"
    "4. The receiving side may disclose submitted information only to authorized officers, employees, advisors, "
    "compliance personnel, or affiliated parties who need such information for preliminary review and who are bound "
    "by confidentiality obligations.\n\n"
    "5. Confidential information shall not be disclosed to unrelated third parties except where such disclosure is required "
    "by law, regulation, court order, or internal compliance obligations.\n\n"
    "6. Submission of this application does not create a financing obligation, partnership, joint venture, agency relationship, "
    "or any final contractual commitment between the parties.\n\n"
    "7. By selecting 'Yes', you confirm that you understand the confidential nature of the submitted information and accept "
    "the above non-circumvention and non-disclosure conditions for the preliminary stage of cooperation.\n\n"
    f"Company details:\n{COMPANY_DETAILS}"
)


def build_summary(data: dict) -> str:
    attachments = data.get("attachments", [])
    attachments_text = ", ".join(
        item["file_name"] for item in attachments if item.get("file_name")
    ) or "No files attached"

    return (
        "APPLICATION SUMMARY\n\n"
        f"Company name: {data.get('company_name', '-')}\n"
        f"Jurisdiction: {data.get('jurisdiction', '-')}\n"
        f"Registration number: {data.get('registration_number', '-')}\n"
        f"Tax number: {data.get('tax_number', '-')}\n"
        f"Contact person: {data.get('contact_person', '-')}\n"
        f"Position: {data.get('position', '-')}\n"
        f"Corporate email: {data.get('corporate_email', '-')}\n"
        f"Phone number: {data.get('phone_number', '-')}\n"
        f"Loan amount: {data.get('loan_amount', '-')}\n"
        f"Currency: {data.get('currency', '-')}\n"
        f"Desired term: {data.get('desired_term', '-')}\n"
        f"Purpose of financing: {data.get('purpose_of_financing', '-')}\n"
        f"Business description: {data.get('business_description', '-')}\n"
        f"Additional comments: {data.get('additional_comments', '-')}\n"
        f"Supporting documents: {attachments_text}"
    )


def build_admin_notification(data: dict, application_id: int, telegram_user_id: int) -> str:
    attachments = data.get("attachments", [])
    attachments_count = len(attachments)

    return (
        "NEW CREDIT APPLICATION\n\n"
        f"Application ID: {application_id}\n"
        f"Status: new\n"
        f"Telegram user ID: {telegram_user_id}\n"
        f"Company name: {data.get('company_name', '-')}\n"
        f"Jurisdiction: {data.get('jurisdiction', '-')}\n"
        f"Registration number: {data.get('registration_number', '-')}\n"
        f"Tax number: {data.get('tax_number', '-')}\n"
        f"Contact person: {data.get('contact_person', '-')}\n"
        f"Position: {data.get('position', '-')}\n"
        f"Corporate email: {data.get('corporate_email', '-')}\n"
        f"Phone number: {data.get('phone_number', '-')}\n"
        f"Loan amount: {data.get('loan_amount', '-')}\n"
        f"Currency: {data.get('currency', '-')}\n"
        f"Desired term: {data.get('desired_term', '-')}\n"
        f"Purpose of financing: {data.get('purpose_of_financing', '-')}\n"
        f"Business description: {data.get('business_description', '-')}\n"
        f"Additional comments: {data.get('additional_comments', '-')}\n"
        f"Attached files: {attachments_count}"
    )


async def show_summary(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.set_state(ApplicationForm.final_confirmation)
    await message.answer(
        build_summary(data),
        reply_markup=final_confirmation_keyboard()
    )
    await message.answer(
        "Please review the summary.\n"
        "Press 'Submit application' to finish, 'Edit' to make changes, or 'Cancel' to stop."
    )


async def return_to_summary_if_editing(message: Message, state: FSMContext) -> bool:
    data = await state.get_data()
    if data.get("editing_mode"):
        await state.update_data(editing_mode=False)
        await show_summary(message, state)
        return True
    return False


@router.message(Command("cancel"))
async def cancel_process(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Application process has been cancelled.",
        reply_markup=main_menu_keyboard()
    )


@router.message(F.text == "Start application")
async def start_application(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(ApplicationForm.confirm_legal_entity)
    await message.answer(
        "Are you submitting this application on behalf of a legal entity?",
        reply_markup=yes_no_keyboard()
    )


@router.message(ApplicationForm.confirm_legal_entity)
async def process_legal_entity_confirmation(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()

    if text not in {"Yes", "No"}:
        await message.answer(
            "Please choose 'Yes' or 'No'.",
            reply_markup=yes_no_keyboard()
        )
        return

    if text == "No":
        await state.clear()
        await message.answer(
            "This bot accepts applications only from legal entities.",
            reply_markup=main_menu_keyboard()
        )
        return

    await state.update_data(confirm_legal_entity=True)
    await state.set_state(ApplicationForm.company_name)
    await message.answer(
        "Please enter the company name.",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(ApplicationForm.company_name)
async def process_company_name(message: Message, state: FSMContext) -> None:
    await state.update_data(company_name=(message.text or "").strip())
    if await return_to_summary_if_editing(message, state):
        return

    await state.set_state(ApplicationForm.jurisdiction)
    await message.answer("Please enter the country or jurisdiction of registration.")


@router.message(ApplicationForm.jurisdiction)
async def process_jurisdiction(message: Message, state: FSMContext) -> None:
    await state.update_data(jurisdiction=(message.text or "").strip())
    if await return_to_summary_if_editing(message, state):
        return

    await state.set_state(ApplicationForm.registration_number)
    await message.answer("Please enter the company registration number.")


@router.message(ApplicationForm.registration_number)
async def process_registration_number(message: Message, state: FSMContext) -> None:
    await state.update_data(registration_number=(message.text or "").strip())
    if await return_to_summary_if_editing(message, state):
        return

    await state.set_state(ApplicationForm.tax_number)
    await message.answer("Please enter the tax number.")


@router.message(ApplicationForm.tax_number)
async def process_tax_number(message: Message, state: FSMContext) -> None:
    await state.update_data(tax_number=(message.text or "").strip())
    if await return_to_summary_if_editing(message, state):
        return

    await state.set_state(ApplicationForm.contact_person)
    await message.answer("Please enter the full name of the contact person.")


@router.message(ApplicationForm.contact_person)
async def process_contact_person(message: Message, state: FSMContext) -> None:
    await state.update_data(contact_person=(message.text or "").strip())
    if await return_to_summary_if_editing(message, state):
        return

    await state.set_state(ApplicationForm.position)
    await message.answer("Please enter the position of the contact person.")


@router.message(ApplicationForm.position)
async def process_position(message: Message, state: FSMContext) -> None:
    await state.update_data(position=(message.text or "").strip())
    if await return_to_summary_if_editing(message, state):
        return

    await state.set_state(ApplicationForm.corporate_email)
    await message.answer("Please enter the corporate email address.")


@router.message(ApplicationForm.corporate_email)
async def process_corporate_email(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()

    if not is_valid_email(value):
        await message.answer(
            "Please enter a valid corporate email address."
        )
        return

    await state.update_data(corporate_email=value)

    if await return_to_summary_if_editing(message, state):
        return

    await state.set_state(ApplicationForm.phone_number)
    await message.answer("Please enter the phone number.")


@router.message(ApplicationForm.phone_number)
async def process_phone_number(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()

    if not is_valid_phone(value):
        await message.answer(
            "Please enter a valid phone number."
        )
        return

    await state.update_data(phone_number=value)

    if await return_to_summary_if_editing(message, state):
        return

    await state.set_state(ApplicationForm.loan_amount)
    await message.answer("Please enter the requested loan amount.")


@router.message(ApplicationForm.loan_amount)
async def process_loan_amount(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    amount = parse_loan_amount(value)

    if amount is None:
        await message.answer(
            "Please enter a valid loan amount greater than 0."
        )
        return

    await state.update_data(loan_amount=f"{amount:.2f}")

    if await return_to_summary_if_editing(message, state):
        return

    await state.set_state(ApplicationForm.currency)
    await message.answer(
        "Please select the currency.",
        reply_markup=currency_keyboard()
    )


@router.message(ApplicationForm.currency)
async def process_currency(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()

    if text not in {"USD", "EUR", "Other"}:
        await message.answer(
            "Please select the currency from the available options.",
            reply_markup=currency_keyboard()
        )
        return

    if text == "Other":
        await state.set_state(ApplicationForm.custom_currency)
        await message.answer(
            "Please enter the currency name.",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    await state.update_data(currency=text)
    if await return_to_summary_if_editing(message, state):
        return

    await state.set_state(ApplicationForm.desired_term)
    await message.answer(
        "Please enter the desired term of financing.",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(ApplicationForm.custom_currency)
async def process_custom_currency(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()

    if not text:
        await message.answer("Please enter the currency name.")
        return

    await state.update_data(currency=text)
    if await return_to_summary_if_editing(message, state):
        return

    await state.set_state(ApplicationForm.desired_term)
    await message.answer("Please enter the desired term of financing.")


@router.message(ApplicationForm.desired_term)
async def process_desired_term(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()

    if not is_valid_desired_term(value):
        await message.answer(
            "Please enter a valid desired term."
        )
        return

    await state.update_data(desired_term=value)

    if await return_to_summary_if_editing(message, state):
        return

    await state.set_state(ApplicationForm.purpose_of_financing)
    await message.answer("Please describe the purpose of financing.")


@router.message(ApplicationForm.purpose_of_financing)
async def process_purpose_of_financing(message: Message, state: FSMContext) -> None:
    await state.update_data(purpose_of_financing=(message.text or "").strip())
    if await return_to_summary_if_editing(message, state):
        return

    await state.set_state(ApplicationForm.business_description)
    await message.answer("Please provide a short business or project description.")


@router.message(ApplicationForm.business_description)
async def process_business_description(message: Message, state: FSMContext) -> None:
    await state.update_data(business_description=(message.text or "").strip())
    if await return_to_summary_if_editing(message, state):
        return

    await state.set_state(ApplicationForm.additional_comments)
    await message.answer(
        "Please enter any additional comments or press 'Skip'.",
        reply_markup=skip_keyboard()
    )


@router.message(ApplicationForm.additional_comments)
async def process_additional_comments(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()

    if text == "Skip":
        text = "No additional comments"

    await state.update_data(additional_comments=text)
    if await return_to_summary_if_editing(message, state):
        return

    await state.update_data(attachments=[])
    await state.set_state(ApplicationForm.supporting_documents)
    await message.answer(
        "Please attach supporting documents.\n"
        "When you finish uploading files, press 'Done'.\n"
        "If you do not want to add files, press 'Skip'.",
        reply_markup=documents_keyboard()
    )


@router.message(ApplicationForm.supporting_documents, F.document)
async def process_document_upload(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    attachments = data.get("attachments", [])

    attachments.append(
        {
            "file_id": message.document.file_id,
            "file_name": message.document.file_name,
        }
    )

    await state.update_data(attachments=attachments)

    await message.answer(
        f"File '{message.document.file_name}' added.\n"
        "You can send another file, press 'Done' to continue, or 'Skip' to continue without more files.",
        reply_markup=documents_keyboard()
    )


@router.message(ApplicationForm.supporting_documents)
async def process_documents_step(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()

    if text not in {"Done", "Skip"}:
        await message.answer(
            "Please send a document, or press 'Done' / 'Skip'.",
            reply_markup=documents_keyboard()
        )
        return

    data = await state.get_data()
    if data.get("editing_mode"):
        await state.update_data(editing_mode=False)
        await show_summary(message, state)
        return

    await state.set_state(ApplicationForm.personal_data_consent)
    await message.answer(
        PERSONAL_DATA_CONSENT_TEXT,
        reply_markup=yes_no_keyboard()
    )


@router.message(ApplicationForm.personal_data_consent)
async def process_personal_data_consent(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()

    if text not in {"Yes", "No"}:
        await message.answer(
            "Please choose 'Yes' or 'No'.",
            reply_markup=yes_no_keyboard()
        )
        return

    if text == "No":
        await state.clear()
        await message.answer(
            "You must accept personal data processing to continue.",
            reply_markup=main_menu_keyboard()
        )
        return

    await state.update_data(personal_data_consent=True)
    await state.set_state(ApplicationForm.ncnd_consent)
    await message.answer(
        NCND_TEXT,
        reply_markup=yes_no_keyboard()
    )


@router.message(ApplicationForm.ncnd_consent)
async def process_ncnd_consent(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()

    if text not in {"Yes", "No"}:
        await message.answer(
            "Please choose 'Yes' or 'No'.",
            reply_markup=yes_no_keyboard()
        )
        return

    if text == "No":
        await state.clear()
        await message.answer(
            "You must accept the NCND conditions to continue.",
            reply_markup=main_menu_keyboard()
        )
        return

    await state.update_data(ncnd_consent=True)
    await show_summary(message, state)


@router.message(ApplicationForm.final_confirmation)
async def process_final_confirmation(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()

    if text == "Cancel":
        await state.clear()
        await message.answer(
            "Application process has been cancelled.",
            reply_markup=main_menu_keyboard()
        )
        return

    if text == "Edit":
        await state.set_state(ApplicationForm.edit_field)
        await message.answer(
            "Please choose what you want to edit.",
            reply_markup=edit_field_keyboard()
        )
        return

    if text != "Submit application":
        await message.answer(
            "Please press 'Submit application', 'Edit', or 'Cancel'.",
            reply_markup=final_confirmation_keyboard()
        )
        return

    data = await state.get_data()
    telegram_user_id = message.from_user.id if message.from_user else 0

    application_id = save_application(data, telegram_user_id)

    if ADMIN_CHAT_ID:
        admin_text = build_admin_notification(data, application_id, telegram_user_id)
        await message.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_text
        )

    await state.clear()
    await message.answer(
        f"Your preliminary credit application has been submitted successfully.\n"
        f"Application ID: {application_id}",
        reply_markup=main_menu_keyboard()
    )


@router.message(ApplicationForm.edit_field)
async def process_edit_field_choice(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()

    if text == "Cancel":
        await state.clear()
        await message.answer(
            "Application process has been cancelled.",
            reply_markup=main_menu_keyboard()
        )
        return

    if text == "Back to summary":
        await show_summary(message, state)
        return

    if text == "Company name":
        await state.update_data(editing_mode=True)
        await state.set_state(ApplicationForm.company_name)
        await message.answer("Please enter the new company name.", reply_markup=ReplyKeyboardRemove())
        return

    if text == "Jurisdiction":
        await state.update_data(editing_mode=True)
        await state.set_state(ApplicationForm.jurisdiction)
        await message.answer("Please enter the new jurisdiction.", reply_markup=ReplyKeyboardRemove())
        return

    if text == "Registration number":
        await state.update_data(editing_mode=True)
        await state.set_state(ApplicationForm.registration_number)
        await message.answer("Please enter the new registration number.", reply_markup=ReplyKeyboardRemove())
        return

    if text == "Tax number":
        await state.update_data(editing_mode=True)
        await state.set_state(ApplicationForm.tax_number)
        await message.answer("Please enter the new tax number.", reply_markup=ReplyKeyboardRemove())
        return

    if text == "Contact person":
        await state.update_data(editing_mode=True)
        await state.set_state(ApplicationForm.contact_person)
        await message.answer("Please enter the new contact person.", reply_markup=ReplyKeyboardRemove())
        return

    if text == "Position":
        await state.update_data(editing_mode=True)
        await state.set_state(ApplicationForm.position)
        await message.answer("Please enter the new position.", reply_markup=ReplyKeyboardRemove())
        return

    if text == "Corporate email":
        await state.update_data(editing_mode=True)
        await state.set_state(ApplicationForm.corporate_email)
        await message.answer("Please enter the new corporate email.", reply_markup=ReplyKeyboardRemove())
        return

    if text == "Phone number":
        await state.update_data(editing_mode=True)
        await state.set_state(ApplicationForm.phone_number)
        await message.answer("Please enter the new phone number.", reply_markup=ReplyKeyboardRemove())
        return

    if text == "Loan amount":
        await state.update_data(editing_mode=True)
        await state.set_state(ApplicationForm.loan_amount)
        await message.answer("Please enter the new loan amount.", reply_markup=ReplyKeyboardRemove())
        return

    if text == "Currency":
        await state.update_data(editing_mode=True)
        await state.set_state(ApplicationForm.currency)
        await message.answer("Please select the new currency.", reply_markup=currency_keyboard())
        return

    if text == "Desired term":
        await state.update_data(editing_mode=True)
        await state.set_state(ApplicationForm.desired_term)
        await message.answer("Please enter the new desired term.", reply_markup=ReplyKeyboardRemove())
        return

    if text == "Purpose of financing":
        await state.update_data(editing_mode=True)
        await state.set_state(ApplicationForm.purpose_of_financing)
        await message.answer("Please enter the new purpose of financing.", reply_markup=ReplyKeyboardRemove())
        return

    if text == "Business description":
        await state.update_data(editing_mode=True)
        await state.set_state(ApplicationForm.business_description)
        await message.answer("Please enter the new business description.", reply_markup=ReplyKeyboardRemove())
        return

    if text == "Additional comments":
        await state.update_data(editing_mode=True)
        await state.set_state(ApplicationForm.additional_comments)
        await message.answer(
            "Please enter the new additional comments or press 'Skip'.",
            reply_markup=skip_keyboard()
        )
        return

    if text == "Supporting documents":
        await state.update_data(editing_mode=True, attachments=[])
        await state.set_state(ApplicationForm.supporting_documents)
        await message.answer(
            "Please re-upload supporting documents.\n"
            "When you finish uploading files, press 'Done'.\n"
            "If you do not want to add files, press 'Skip'.",
            reply_markup=documents_keyboard()
        )
        return

    await message.answer(
        "Please choose a field from the list.",
        reply_markup=edit_field_keyboard()
    )
