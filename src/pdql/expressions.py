from typing import Any, Union, Optional, List
from pdql.dialects import Dialect


class SQLNode:
    """Base class for SQL syntax tree nodes."""

    def to_sql(self, dialect: Dialect) -> str:
        raise NotImplementedError

    def _op(self, op: str, other: Any) -> "SQLExpression":
        return SQLExpression(self, op, other)

    def __eq__(self, other: Any) -> "SQLExpression":  # type: ignore
        return self._op("eq", other)

    def __ne__(self, other: Any) -> "SQLExpression":  # type: ignore
        return self._op("ne", other)

    def __lt__(self, other: Any) -> "SQLExpression":
        return self._op("lt", other)

    def __le__(self, other: Any) -> "SQLExpression":
        return self._op("le", other)

    def __gt__(self, other: Any) -> "SQLExpression":
        return self._op("gt", other)

    def __ge__(self, other: Any) -> "SQLExpression":
        return self._op("ge", other)

    def __add__(self, other: Any) -> "SQLExpression":
        return self._op("add", other)

    def __sub__(self, other: Any) -> "SQLExpression":
        return self._op("sub", other)

    def __mul__(self, other: Any) -> "SQLExpression":
        return self._op("mul", other)

    def __truediv__(self, other: Any) -> "SQLExpression":
        return self._op("div", other)

    def __and__(self, other: Any) -> "SQLExpression":
        return self._op("and", other)

    def __or__(self, other: Any) -> "SQLExpression":
        return self._op("or", other)


class SQLExpression(SQLNode):
    """Represents a binary operation in SQL."""

    def __init__(self, left: Union[SQLNode, Any], op: str, right: Union[SQLNode, Any]):
        self.left = left
        self.op = op
        self.right = right

    def to_sql(self, dialect: Dialect) -> str:
        left_sql = (
            self.left.to_sql(dialect)
            if isinstance(self.left, SQLNode)
            else dialect.format_value(self.left)
        )
        right_sql = (
            self.right.to_sql(dialect)
            if isinstance(self.right, SQLNode)
            else dialect.format_value(self.right)
        )
        operator = dialect.translate_op(self.op)
        return f"({left_sql} {operator} {right_sql})"


class SQLColumn(SQLNode):
    """Represents a column in a SQL table."""

    def __init__(self, name: str, owner: Optional[str] = None):
        self.name = name
        self.owner = owner

    def to_sql(self, dialect: Dialect) -> str:
        col = dialect.quote_identifier(self.name)
        if self.owner:
            owner = dialect.quote_identifier(self.owner)
            return f"{owner}.{col}"
        return col


class SQLFunction(SQLNode):
    """Represents a SQL function."""

    def __init__(
        self,
        name: str,
        args: Optional[Union[List[Any], Any]] = None,
        alias: Optional[str] = None,
    ):
        self.name = name
        if args is None:
            self.args = []
        elif isinstance(args, list):
            self.args = args
        else:
            self.args = [args]
        self.alias = alias

    def to_sql(self, dialect: Dialect) -> str:
        func_name = dialect.translate_function(self.name)
        arg_sqls = []
        for arg in self.args:
            if isinstance(arg, SQLNode):
                arg_sqls.append(arg.to_sql(dialect))
            elif arg == "*":
                arg_sqls.append("*")
            else:
                arg_sqls.append(dialect.format_value(arg))

        args_str = ", ".join(arg_sqls)
        sql = f"{func_name}({args_str})"

        if self.alias:
            return f"{sql} AS {dialect.quote_identifier(self.alias)}"
        return sql

    def over(self, partition_by=None, order_by=None) -> "SQLWindowFunction":
        return SQLWindowFunction(self, partition_by=partition_by, order_by=order_by)


class SQLWindowFunction(SQLNode):
    """Represents a Window Function."""

    def __init__(
        self,
        func: SQLFunction,
        partition_by: Optional[Union[List[Any], Any]] = None,
        order_by: Optional[Union[List[Any], Any]] = None,
    ):
        self.func = func

        if partition_by is None:
            self.partition_by = []
        elif isinstance(partition_by, list):
            self.partition_by = partition_by
        else:
            self.partition_by = [partition_by]

        if order_by is None:
            self.order_by = []
        elif isinstance(order_by, list):
            self.order_by = order_by
        else:
            self.order_by = [order_by]

        self.alias = func.alias
        self.func.alias = None

    def to_sql(self, dialect: Dialect) -> str:
        func_sql = self.func.to_sql(dialect)

        parts = []
        if self.partition_by:
            p_sqls = []
            for p in self.partition_by:
                if isinstance(p, SQLNode):
                    p_sqls.append(p.to_sql(dialect))
                else:
                    p_sqls.append(dialect.quote_identifier(str(p)))
            parts.append(f"PARTITION BY {', '.join(p_sqls)}")

        if self.order_by:
            o_sqls = []
            for o in self.order_by:
                if isinstance(o, SQLNode):
                    o_sqls.append(o.to_sql(dialect))
                else:
                    o_sqls.append(dialect.quote_identifier(str(o)))
            parts.append(f"ORDER BY {', '.join(o_sqls)}")

        over_clause = " ".join(parts)
        sql = f"{func_sql} OVER ({over_clause})"

        if self.alias:
            return f"{sql} AS {dialect.quote_identifier(self.alias)}"
        return sql
