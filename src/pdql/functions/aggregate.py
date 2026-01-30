from typing import Any, Optional
from pdql.expressions import SQLFunction


def any_value(expression: Any) -> SQLFunction:
    """Gets an expression for some row."""
    return SQLFunction("ANY_VALUE", expression)


def approx_count_distinct(expression: Any) -> SQLFunction:
    """Gets the approximate result for COUNT(DISTINCT expression)."""
    return SQLFunction("APPROX_COUNT_DISTINCT", expression)


def array_agg(expression: Any, is_distinct: bool = False) -> SQLFunction:
    """Gets an array of values."""
    return SQLFunction("ARRAY_AGG", expression, is_distinct=is_distinct)


def avg(expression: Any, is_distinct: bool = False) -> SQLFunction:
    """Gets the average of non-NULL values."""
    return SQLFunction("AVG", expression, is_distinct=is_distinct)


def count(expression: Any = "*", is_distinct: bool = False) -> SQLFunction:
    """Gets the number of rows or non-NULL values."""
    return SQLFunction("COUNT", expression, is_distinct=is_distinct)


def countif(expression: Any) -> SQLFunction:
    """Gets the number of TRUE values for an expression."""
    return SQLFunction("COUNTIF", expression)


def logical_and(expression: Any) -> SQLFunction:
    """Gets the logical AND of all non-NULL expressions."""
    return SQLFunction("LOGICAL_AND", expression)


def logical_or(expression: Any) -> SQLFunction:
    """Gets the logical OR of all non-NULL expressions."""
    return SQLFunction("LOGICAL_OR", expression)


def max(expression: Any) -> SQLFunction:
    """Gets the maximum non-NULL value."""
    return SQLFunction("MAX", expression)


def min(expression: Any) -> SQLFunction:
    """Gets the minimum non-NULL value."""
    return SQLFunction("MIN", expression)


def string_agg(expression: Any, delimiter: str = ",", is_distinct: bool = False) -> SQLFunction:
    """Concatenates non-NULL STRING or BYTES values."""
    return SQLFunction("STRING_AGG", [expression, delimiter], is_distinct=is_distinct)


def sum(expression: Any, is_distinct: bool = False) -> SQLFunction:
    """Gets the sum of non-NULL values."""
    return SQLFunction("SUM", expression, is_distinct=is_distinct)
