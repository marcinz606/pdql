from abc import ABC, abstractmethod
from typing import Any, Dict


class Dialect(ABC):
    """Abstract base class for SQL dialects."""

    def __init__(self):
        self.function_mapping: Dict[str, str] = {
            "mean": "AVG",
            "sum": "SUM",
            "count": "COUNT",
            "min": "MIN",
            "max": "MAX",
        }

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
        return self.function_mapping.get(name.lower(), name.upper())

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
    def __init__(self):
        super().__init__()
        # Example of dialect specific mapping
        self.function_mapping.update({
            "len": "LENGTH",
            "char_length": "LENGTH",
        })

    def quote_identifier(self, name: str) -> str:
        return f'"{name}"'


class BigQueryDialect(Dialect):
    def __init__(self):
        super().__init__()
        self.function_mapping.update({
            "len": "LENGTH",
        })

    def quote_identifier(self, name: str) -> str:
        return f"`{name}`"