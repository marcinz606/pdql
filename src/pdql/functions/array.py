from typing import Any, List, Optional
from pdql.expressions import SQLFunction


def array(*args: Any) -> SQLFunction:
    """Produces an array with one element for each row in a subquery or list."""
    return SQLFunction("ARRAY", list(args))


def array_concat(*args: Any) -> SQLFunction:
    """Concatenates one or more arrays into a single array."""
    return SQLFunction("ARRAY_CONCAT", list(args))


def array_length(array_expression: Any) -> SQLFunction:
    """Gets the number of elements in an array."""
    return SQLFunction("ARRAY_LENGTH", array_expression)


def array_reverse(array_expression: Any) -> SQLFunction:
    """Reverses the order of elements in an array."""
    return SQLFunction("ARRAY_REVERSE", array_expression)


def array_to_string(array_expression: Any, delimiter: str, null_text: Optional[str] = None) -> SQLFunction:
    """Produces a concatenation of the elements in an array as a STRING value."""
    args = [array_expression, delimiter]
    if null_text is not None:
        args.append(null_text)
    return SQLFunction("ARRAY_TO_STRING", args)


def generate_array(start: Any, end: Any, step: Optional[Any] = None) -> SQLFunction:
    """Generates an array of values in a range."""
    args = [start, end]
    if step is not None:
        args.append(step)
    return SQLFunction("GENERATE_ARRAY", args)
