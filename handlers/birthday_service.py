"""Birthday service: find contacts with birthdays within a given number of days."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import date, datetime, timedelta
from typing import Any

from models.contact import Record

DATE_OUTPUT_FORMAT = "%d.%m.%Y"
WEEKDAY_OUTPUT_FORMAT = "%A"


class BirthdayService:
    """Service to find contacts with birthdays within a specified number of days."""

    def __init__(self, repository) -> None:
        """Initialize the service with a contact repository.
        
        Args:
            repository: ContactRepository instance with get_all_contacts() method
        """
        self._repository = repository

    def find_near(self, days: int) -> list[dict[str, Any]]:
        """Find contacts with birthdays within the specified number of days.
        
        Args:
            days: Number of days from today (must be non-negative)
            
        Returns:
            List of dictionaries with contact information and congratulation dates
            
        Raises:
            ValueError: If days is negative
        """
        if days < 0:
            raise ValueError("Parameter 'days' must be non-negative.")
        
        window = self._build_window(days)
        records = self._collect_records(window)
        return self._format_records(records)

    def _collect_records(
        self, window: Mapping[tuple[int, int], date]
    ) -> list[tuple[date, Record]]:
        """Collect contacts whose birthdays fall within the date window.
        
        Args:
            window: Dictionary mapping (month, day) tuples to actual dates
            
        Returns:
            List of tuples (congratulation_date, contact)
        """
        records: list[tuple[date, Record]] = []
        
        for contact in self._repository.get_all_contacts():
            if contact.birthday is None:
                continue
            
            try:
                birthday = self._ensure_date(contact.birthday)
            except (TypeError, ValueError):
                continue
            
            actual_date = window.get((birthday.month, birthday.day))
            if actual_date is None:
                continue
            
            records.append((self._shift_to_monday(actual_date), contact))
        
        return records

    def _format_records(
        self, records: list[tuple[date, Record]]
    ) -> list[dict[str, Any]]:
        """Format records for output, sorted by date and name.
        
        Args:
            records: List of (date, contact) tuples
            
        Returns:
            List of formatted dictionaries
        """
        ordered = sorted(
            records,
            key=lambda record: (
                record[0],
                record[1].name.value.lower(),
            ),
        )
        
        formatted = []
        for congratulation_date, contact in ordered:
            phones = [p.value for p in contact.phones]
            emails = [e.value for e in contact.emails]
            
            formatted.append({
                "date": congratulation_date.strftime(DATE_OUTPUT_FORMAT),
                "weekday": congratulation_date.strftime(WEEKDAY_OUTPUT_FORMAT),
                "name": contact.name.value,
                "phone": phones[0] if phones else "",
                "email": emails[0] if emails else "",
                "phones": phones,
                "emails": emails,
            })
        
        return formatted

    @staticmethod
    def _build_window(days: int) -> Mapping[tuple[int, int], date]:
        """Build a date window mapping (month, day) to actual dates.
        
        Args:
            days: Number of days from today
            
        Returns:
            Dictionary mapping (month, day) tuples to date objects
        """
        today = date.today()
        return {
            (current.month, current.day): current
            for current in (today + timedelta(days=offset) for offset in range(days + 1))
        }

    @staticmethod
    def _shift_to_monday(candidate: date) -> date:
        """Shift weekend dates to Monday for congratulation scheduling.
        
        Args:
            candidate: Original date
            
        Returns:
            Date shifted to Monday if weekend, otherwise original date
        """
        weekday = candidate.weekday()
        if weekday == 5:  # Saturday
            return candidate + timedelta(days=2)
        if weekday == 6:  # Sunday
            return candidate + timedelta(days=1)
        return candidate

    @staticmethod
    def _ensure_date(raw_value: Any) -> date:
        """Convert various birthday formats to a date object.
        
        Args:
            raw_value: Birthday value (Birthday object, datetime, date, or string)
            
        Returns:
            date object
            
        Raises:
            TypeError: If value cannot be converted to date
            ValueError: If string format is unsupported
        """
        if raw_value is None:
            raise TypeError("Birthday value is missing.")
        
        # Handle Birthday model object (has .value attribute)
        if hasattr(raw_value, "value"):
            return BirthdayService._ensure_date(getattr(raw_value, "value"))
        
        # Handle dictionary with "value" key
        if isinstance(raw_value, Mapping) and "value" in raw_value:
            return BirthdayService._ensure_date(raw_value["value"])
        
        # Handle date objects
        if isinstance(raw_value, date) and not isinstance(raw_value, datetime):
            return raw_value
        
        # Handle datetime objects
        if isinstance(raw_value, datetime):
            return raw_value.date()
        
        # Handle string dates
        if isinstance(raw_value, str):
            return BirthdayService._parse_date_string(raw_value)
        
        raise TypeError(
            "Birthday values must be date, datetime, or string. "
            f"Received: {type(raw_value)!r}"
        )

    @staticmethod
    def _parse_date_string(value: str) -> date:
        """Parse a date string in supported formats.
        
        Args:
            value: Date string
            
        Returns:
            date object
            
        Raises:
            ValueError: If format is not supported
        """
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

