from typing import Any, List, Optional
from pdql.expressions import SQLFunction


def ascii(value: Any) -> SQLFunction:
    """Gets the ASCII code for the first character or byte in a STRING or BYTES value."""
    return SQLFunction("ASCII", value)


def byte_length(value: Any) -> SQLFunction:
    """Gets the number of BYTES in a STRING or BYTES value."""
    return SQLFunction("BYTE_LENGTH", value)


def char_length(value: Any) -> SQLFunction:
    """Gets the number of characters in a STRING value."""
    return SQLFunction("CHAR_LENGTH", value)


def character_length(value: Any) -> SQLFunction:
    """Synonym for CHAR_LENGTH."""
    return SQLFunction("CHARACTER_LENGTH", value)


def chr(value: Any) -> SQLFunction:
    """Converts a Unicode code point to a character."""
    return SQLFunction("CHR", value)


def concat(*args: Any) -> SQLFunction:
    """Concatenates one or more STRING or BYTES values into a single result."""
    return SQLFunction("CONCAT", list(args))


def ends_with(value: Any, suffix: Any) -> SQLFunction:
    """Checks if a STRING or BYTES value is the suffix of another value."""
    return SQLFunction("ENDS_WITH", [value, suffix])


def initcap(value: Any) -> SQLFunction:
    """Formats a STRING as proper case."""
    return SQLFunction("INITCAP", value)


def instr(source: Any, target: Any, pos: Optional[Any] = None, occurrence: Optional[Any] = None) -> SQLFunction:
    """Finds the position of a subvalue inside another value."""
    args = [source, target]
    if pos is not None:
        args.append(pos)
        if occurrence is not None:
            args.append(occurrence)
    return SQLFunction("INSTR", args)


def left(value: Any, length: Any) -> SQLFunction:
    """Gets the specified leftmost portion from a STRING or BYTES value."""
    return SQLFunction("LEFT", [value, length])


def length(value: Any) -> SQLFunction:
    """Gets the length of a STRING or BYTES value."""
    return SQLFunction("LENGTH", value)


def lower(value: Any) -> SQLFunction:
    """Formats alphabetic characters in a STRING value as lowercase."""
    return SQLFunction("LOWER", value)


def lpad(value: Any, length: Any, pattern: Optional[Any] = None) -> SQLFunction:
    """Prepends a STRING or BYTES value with a pattern."""
    args = [value, length]
    if pattern is not None:
        args.append(pattern)
    return SQLFunction("LPAD", args)


def ltrim(value: Any, trim_set: Optional[Any] = None) -> SQLFunction:
    """Removes leading characters."""
    if trim_set is not None:
        return SQLFunction("LTRIM", [value, trim_set])
    return SQLFunction("LTRIM", value)


def regexp_contains(value: Any, regexp: Any) -> SQLFunction:
    """Checks if a value is a partial match for a regular expression."""
    return SQLFunction("REGEXP_CONTAINS", [value, regexp])


def regexp_extract(value: Any, regexp: Any) -> SQLFunction:
    """Produces a substring that matches a regular expression."""
    return SQLFunction("REGEXP_EXTRACT", [value, regexp])


def regexp_replace(value: Any, regexp: Any, replacement: Any) -> SQLFunction:
    """Replaces all substrings that match a regular expression."""
    return SQLFunction("REGEXP_REPLACE", [value, regexp, replacement])


def repeat(value: Any, count: Any) -> SQLFunction:
    """Produces a STRING or BYTES value that consists of an original value, repeated."""
    return SQLFunction("REPEAT", [value, count])


def replace(value: Any, old_pattern: Any, new_pattern: Any) -> SQLFunction:
    """Replaces all occurrences of a pattern with another pattern."""
    return SQLFunction("REPLACE", [value, old_pattern, new_pattern])


def reverse(value: Any) -> SQLFunction:
    """Reverses a STRING or BYTES value."""
    return SQLFunction("REVERSE", value)


def right(value: Any, length: Any) -> SQLFunction:
    """Gets the specified rightmost portion from a STRING or BYTES value."""
    return SQLFunction("RIGHT", [value, length])


def rpad(value: Any, length: Any, pattern: Optional[Any] = None) -> SQLFunction:
    """Appends a STRING or BYTES value with a pattern."""
    args = [value, length]
    if pattern is not None:
        args.append(pattern)
    return SQLFunction("RPAD", args)


def rtrim(value: Any, trim_set: Optional[Any] = None) -> SQLFunction:
    """Removes trailing characters."""
    if trim_set is not None:
        return SQLFunction("RTRIM", [value, trim_set])
    return SQLFunction("RTRIM", value)


def split(value: Any, delimiter: Any) -> SQLFunction:
    """Splits a STRING or BYTES value, using a delimiter."""
    return SQLFunction("SPLIT", [value, delimiter])


def starts_with(value: Any, prefix: Any) -> SQLFunction:
    """Checks if a STRING or BYTES value is a prefix of another value."""
    return SQLFunction("STARTS_WITH", [value, prefix])


def strpos(value: Any, sub: Any) -> SQLFunction:
    """Finds the position of the first occurrence of a subvalue."""
    return SQLFunction("STRPOS", [value, sub])


def substr(value: Any, pos: Any, length: Optional[Any] = None) -> SQLFunction:
    """Gets a portion of a STRING or BYTES value."""
    args = [value, pos]
    if length is not None:
        args.append(length)
    return SQLFunction("SUBSTR", args)


def trim(value: Any, trim_set: Optional[Any] = None) -> SQLFunction:
    """Removes leading and trailing characters."""
    if trim_set is not None:
        return SQLFunction("TRIM", [value, trim_set])
    return SQLFunction("TRIM", value)


def upper(value: Any) -> SQLFunction:
    """Formats alphabetic characters in a STRING value as uppercase."""
    return SQLFunction("UPPER", value)
