from typing import Any, Optional
from pdql.expressions import SQLFunction


def json_array(*args: Any) -> SQLFunction:
    """Creates a JSON array."""
    return SQLFunction("JSON_ARRAY", list(args))


def json_extract(json_string: Any, json_path: str) -> SQLFunction:
    """Extracts a JSON value and converts it to a SQL JSON-formatted STRING or JSON value."""
    return SQLFunction("JSON_EXTRACT", [json_string, json_path])


def json_extract_array(json_string: Any, json_path: Optional[str] = None) -> SQLFunction:
    """Extracts a JSON array."""
    args = [json_string]
    if json_path:
        args.append(json_path)
    return SQLFunction("JSON_EXTRACT_ARRAY", args)


def json_extract_scalar(json_string: Any, json_path: str) -> SQLFunction:
    """Extracts a JSON scalar value and converts it to a SQL STRING value."""
    return SQLFunction("JSON_EXTRACT_SCALAR", [json_string, json_path])


def json_query(json_string: Any, json_path: str) -> SQLFunction:
    """Extracts a JSON value."""
    return SQLFunction("JSON_QUERY", [json_string, json_path])


def json_type(json_string: Any, json_path: Optional[str] = None) -> SQLFunction:
    """Gets the JSON type of the outermost JSON value."""
    args = [json_string]
    if json_path:
        args.append(json_path)
    return SQLFunction("JSON_TYPE", args)


def json_value(json_string: Any, json_path: str) -> SQLFunction:
    """Extracts a JSON scalar value and converts it to a SQL STRING value."""
    return SQLFunction("JSON_VALUE", [json_string, json_path])


def to_json(value: Any) -> SQLFunction:
    """Converts a SQL value to a JSON value."""
    return SQLFunction("TO_JSON", value)


def to_json_string(value: Any) -> SQLFunction:
    """Converts a SQL value to a JSON-formatted STRING value."""
    return SQLFunction("TO_JSON_STRING", value)
