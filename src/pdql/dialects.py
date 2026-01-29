from abc import ABC, abstractmethod
from typing import Any


class Dialect(ABC):
    """Abstract base class for SQL dialects."""

    @abstractmethod
    def quote_identifier(self, name: str) -> str:
        pass

    def format_value(self, value: Any) -> str:
        if isinstance(value, str):
            escaped = value.replace("'", "''")
            return f"'{escaped}'"
        if value is None:
            return "NULL"
        if isinstance(value, bool):
            return "TRUE" if value else "FALSE"
        return str(value)

    def translate_function(self, name: str) -> str:
        mapping = {
            "mean": "AVG",
            "sum": "SUM",
            "count": "COUNT",
            "min": "MIN",
            "max": "MAX",
        }
        return mapping.get(name.lower(), name.upper())

    def translate_op(self, op: str) -> str:
        mapping = {
            "eq": "=",
            "ne": "!=",
            "gt": ">",
            "lt": "<",
            "ge": ">=",
            "le": "<=",
            "add": "+",
            "sub": "-",
            "mul": "*",
            "div": "/",
            "and": "AND",
            "or": "OR",
        }
        return mapping.get(op, op)


class GenericDialect(Dialect):
    def quote_identifier(self, name: str) -> str:
        return f'"{name}"'


class PostgresDialect(Dialect):
    def quote_identifier(self, name: str) -> str:
        return f'"{name}"'


class BigQueryDialect(Dialect):
    def quote_identifier(self, name: str) -> str:
        return f"`{name}`"
