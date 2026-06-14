import sqlite3
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "data"
DB_PATH = DB_DIR / "applications.db"

ALLOWED_STATUSES = {
    "new",
    "in_review",
    "contacted",
    "rejected",
    "approved_next_step",
}


def get_connection() -> sqlite3.Connection:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                company_name TEXT NOT NULL,
                jurisdiction TEXT NOT NULL,
                registration_number TEXT NOT NULL,
                tax_number TEXT NOT NULL,
                contact_person TEXT NOT NULL,
                position TEXT NOT NULL,
                corporate_email TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                loan_amount TEXT NOT NULL,
                currency TEXT NOT NULL,
                desired_term TEXT NOT NULL,
                purpose_of_financing TEXT NOT NULL,
                business_description TEXT NOT NULL,
                additional_comments TEXT,
                personal_data_consent INTEGER NOT NULL,
                ncnd_consent INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'new'
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS application_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id INTEGER NOT NULL,
                telegram_file_id TEXT NOT NULL,
                file_name TEXT,
                FOREIGN KEY (application_id) REFERENCES applications (id)
            )
            """
        )

        cursor.execute("PRAGMA table_info(applications)")
        columns = [row["name"] for row in cursor.fetchall()]

        if "status" not in columns:
            cursor.execute(
                """
                ALTER TABLE applications
                ADD COLUMN status TEXT NOT NULL DEFAULT 'new'
                """
            )

        connection.commit()


def save_application(data: dict[str, Any], telegram_user_id: int) -> int:
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO applications (
                telegram_user_id,
                company_name,
                jurisdiction,
                registration_number,
                tax_number,
                contact_person,
                position,
                corporate_email,
                phone_number,
                loan_amount,
                currency,
                desired_term,
                purpose_of_financing,
                business_description,
                additional_comments,
                personal_data_consent,
                ncnd_consent,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                telegram_user_id,
                data.get("company_name", ""),
                data.get("jurisdiction", ""),
                data.get("registration_number", ""),
                data.get("tax_number", ""),
                data.get("contact_person", ""),
                data.get("position", ""),
                data.get("corporate_email", ""),
                data.get("phone_number", ""),
                data.get("loan_amount", ""),
                data.get("currency", ""),
                data.get("desired_term", ""),
                data.get("purpose_of_financing", ""),
                data.get("business_description", ""),
                data.get("additional_comments", ""),
                1 if data.get("personal_data_consent") else 0,
                1 if data.get("ncnd_consent") else 0,
                "new",
            ),
        )

        application_id = cursor.lastrowid

        attachments = data.get("attachments", [])
        for attachment in attachments:
            cursor.execute(
                """
                INSERT INTO application_files (
                    application_id,
                    telegram_file_id,
                    file_name
                )
                VALUES (?, ?, ?)
                """,
                (
                    application_id,
                    attachment.get("file_id", ""),
                    attachment.get("file_name", ""),
                ),
            )

        connection.commit()
        return int(application_id)


def get_recent_applications(limit: int = 10) -> list[sqlite3.Row]:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT
                id,
                created_at,
                company_name,
                contact_person,
                loan_amount,
                currency,
                status
            FROM applications
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )
        return cursor.fetchall()


def get_application_by_id(application_id: int) -> sqlite3.Row | None:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT *
            FROM applications
            WHERE id = ?
            """,
            (application_id,),
        )
        return cursor.fetchone()


def get_files_by_application_id(application_id: int) -> list[sqlite3.Row]:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id, telegram_file_id, file_name
            FROM application_files
            WHERE application_id = ?
            ORDER BY id ASC
            """,
            (application_id,),
        )
        return cursor.fetchall()


def update_application_status(application_id: int, status: str) -> bool:
    if status not in ALLOWED_STATUSES:
        return False

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE applications
            SET status = ?
            WHERE id = ?
            """,
            (status, application_id),
        )
        connection.commit()
        return cursor.rowcount > 0


def get_applications_by_status(status: str, limit: int = 10) -> list[sqlite3.Row]:
    if status not in ALLOWED_STATUSES:
        return []

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT
                id,
                created_at,
                company_name,
                contact_person,
                loan_amount,
                currency,
                status
            FROM applications
            WHERE status = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (status, limit),
        )
        return cursor.fetchall()
