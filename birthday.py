"""Birthday utilities: filter normalised contacts by dates and prepare output."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from datetime import date, datetime, timedelta
from typing import Any, Protocol, cast

DATE_OUTPUT_FORMAT = "%d.%m.%Y"
WEEKDAY_OUTPUT_FORMAT = "%A"


class ContactProtocol(Protocol):
    name: str
    phones: Sequence[str]
    emails: Sequence[str]
    birthday: date | datetime | str


class ContactsRepositoryProtocol(Protocol):
    def get_all_contacts(self) -> Iterable[ContactProtocol]: ...


class ContactsGatewayProtocol(Protocol):
    def get_contacts(self) -> Iterable[ContactProtocol]: ...


def _get_attribute(contact: ContactProtocol, attr: str, default: Any = None) -> Any:
    if hasattr(contact, attr):
        return getattr(contact, attr)
    if isinstance(contact, Mapping):
        return contact.get(attr, default)
    return default


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [str(item) for item in value if item not in (None, "")]
    return [str(value)]


class BirthdayFormatter:
    def __init__(
        self,
        date_format: str = DATE_OUTPUT_FORMAT,
        weekday_format: str = WEEKDAY_OUTPUT_FORMAT,
    ) -> None:
        self._date_format = date_format
        self._weekday_format = weekday_format

    def format(self, contact: ContactProtocol, congratulation_date: date) -> dict[str, Any]:
        name = str(_get_attribute(contact, "name", ""))
        phones = _as_list(_get_attribute(contact, "phones", []))
        emails = _as_list(_get_attribute(contact, "emails", []))
        return {
            "date": congratulation_date.strftime(self._date_format),
            "weekday": congratulation_date.strftime(self._weekday_format),
            "name": name,
            "phone": phones[0] if phones else "",
            "email": emails[0] if emails else "",
            "phones": phones,
            "emails": emails,
        }


class RepositoryContactsGateway(ContactsGatewayProtocol):
    def __init__(self, repository: ContactsRepositoryProtocol) -> None:
        self._repository = repository

    def get_contacts(self) -> Iterable[ContactProtocol]:
        contacts = self._repository.get_all_contacts()
        if isinstance(contacts, Mapping):
            return contacts.values()
        return contacts


class BirthdayService:
    def __init__(
        self,
        contacts_source: ContactsGatewayProtocol | ContactsRepositoryProtocol,
        formatter: BirthdayFormatter | None = None,
    ) -> None:
        self._contacts_gateway = self._ensure_gateway(contacts_source)
        self._formatter = formatter or BirthdayFormatter()

    def find_near(self, days: int) -> list[dict[str, Any]]:
        if days < 0:
            raise ValueError("Parameter 'days' must be non-negative.")
        window = self._build_window(days)
        records = self._collect_records(window)
        return self._format_records(records)

    def find_date(self, target_date: date | datetime | str) -> list[dict[str, Any]]:
        normalized_date = self._ensure_date(target_date)
        window = {(normalized_date.month, normalized_date.day): normalized_date}
        records = self._collect_records(window)
        return self._format_records(records)

    def _collect_records(
        self, window: Mapping[tuple[int, int], date]
    ) -> list[tuple[date, ContactProtocol]]:
        records: list[tuple[date, ContactProtocol]] = []
        for contact in self._contacts_gateway.get_contacts():
            raw_birthday = _get_attribute(contact, "birthday")
            if raw_birthday is None:
                continue
            try:
                birthday = self._ensure_date(raw_birthday)
            except (TypeError, ValueError):
                continue
            actual_date = window.get((birthday.month, birthday.day))
            if actual_date is None:
                continue
            records.append((self._shift_to_monday(actual_date), contact))
        return records

    def _format_records(
        self, records: list[tuple[date, ContactProtocol]]
    ) -> list[dict[str, Any]]:
        ordered = sorted(
            records,
            key=lambda record: (
                record[0],
                str(_get_attribute(record[1], "name", "")).lower(),
            ),
        )
        return [
            self._formatter.format(contact, congratulation_date)
            for congratulation_date, contact in ordered
        ]

    @staticmethod
    def _build_window(days: int) -> Mapping[tuple[int, int], date]:
        today = date.today()
        return {
            (current.month, current.day): current
            for current in (today + timedelta(days=offset) for offset in range(days + 1))
        }

    @staticmethod
    def _shift_to_monday(candidate: date) -> date:
        weekday = candidate.weekday()
        if weekday == 5:
            return candidate + timedelta(days=2)
        if weekday == 6:
            return candidate + timedelta(days=1)
        return candidate

    @staticmethod
    def _ensure_date(raw_value: Any) -> date:
        if raw_value is None:
            raise TypeError("Birthday value is missing.")
        if hasattr(raw_value, "value"):
            return BirthdayService._ensure_date(getattr(raw_value, "value"))
        if isinstance(raw_value, Mapping) and "value" in raw_value:
            return BirthdayService._ensure_date(raw_value["value"])
        if isinstance(raw_value, date) and not isinstance(raw_value, datetime):
            return raw_value
        if isinstance(raw_value, datetime):
            return raw_value.date()
        if isinstance(raw_value, str):
            return BirthdayService._parse_date_string(raw_value)
        raise TypeError(
            "Birthday values must be date, datetime, or string. "
            f"Received: {type(raw_value)!r}"
        )

    @staticmethod
    def _parse_date_string(value: str) -> date:
        supported_formats = ("%Y-%m-%d", "%Y.%m.%d", "%d.%m.%Y")
        for fmt in supported_formats:
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
        try:
            return datetime.fromisoformat(value).date()
        except ValueError:
            pass
        raise ValueError(
            "Unsupported date format. "
            f"Expected one of: {', '.join(supported_formats)}. Got: {value!r}"
        )

    @staticmethod
    def _ensure_gateway(
        source: ContactsGatewayProtocol | ContactsRepositoryProtocol,
    ) -> ContactsGatewayProtocol:
        get_contacts = getattr(source, "get_contacts", None)
        if callable(get_contacts):
            return cast(ContactsGatewayProtocol, source)
        get_all = getattr(source, "get_all_contacts", None)
        if callable(get_all):
            return RepositoryContactsGateway(source)  # type: ignore[arg-type]
        raise TypeError(
            "contacts_source must implement 'get_contacts' or 'get_all_contacts'."
        )


def build_birthday_service(
    repository: ContactsRepositoryProtocol,
    formatter: BirthdayFormatter | None = None,
) -> BirthdayService:
    return BirthdayService(RepositoryContactsGateway(repository), formatter)

