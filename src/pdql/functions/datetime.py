from typing import Any, Optional
from pdql.expressions import SQLFunction


def current_date() -> SQLFunction:
    """Returns the current date as a DATE value."""
    return SQLFunction("CURRENT_DATE")


def current_datetime() -> SQLFunction:
    """Returns the current date and time as a DATETIME value."""
    return SQLFunction("CURRENT_DATETIME")


def current_time() -> SQLFunction:
    """Returns the current time as a TIME value."""
    return SQLFunction("CURRENT_TIME")


def current_timestamp() -> SQLFunction:
    """Returns the current date and time as a TIMESTAMP object."""
    return SQLFunction("CURRENT_TIMESTAMP")


def date(year: Any, month: Optional[Any] = None, day: Optional[Any] = None) -> SQLFunction:
    """Constructs a DATE value."""
    if month is None:
        return SQLFunction("DATE", year)
    return SQLFunction("DATE", [year, month, day])


def date_add(date_expression: Any, interval: str) -> SQLFunction:
    """Adds a specified time interval to a DATE value."""
    return SQLFunction("DATE_ADD", [date_expression, interval], special_format="DATE_ADD({args})")


def date_diff(date_a: Any, date_b: Any, part: str) -> SQLFunction:
    """Gets the number of unit boundaries between two DATE values."""
    return SQLFunction("DATE_DIFF", [date_a, date_b, part])


def date_trunc(date_expression: Any, part: str) -> SQLFunction:
    """Truncates a DATE value."""
    return SQLFunction("DATE_TRUNC", [date_expression, part])


def extract(part: str, expression: Any) -> SQLFunction:
    """Extracts part of a date/time value."""
    return SQLFunction("EXTRACT", [expression], special_format=f"EXTRACT({part} FROM {{args}})")


def format_date(format_string: str, date_expr: Any) -> SQLFunction:
    """Formats a DATE value according to a specified format string."""
    return SQLFunction("FORMAT_DATE", [format_string, date_expr])


def parse_date(format_string: str, date_string: Any) -> SQLFunction:
    """Converts a STRING value to a DATE value."""
    return SQLFunction("PARSE_DATE", [format_string, date_string])


def unix_date(date_expr: Any) -> SQLFunction:
    """Converts a DATE value to the number of days since 1970-01-01."""
    return SQLFunction("UNIX_DATE", date_expr)
