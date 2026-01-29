import uuid
from typing import List, Optional, Union, Any, Dict, Tuple
from dataclasses import dataclass
from pdql.expressions import SQLColumn, SQLExpression, SQLNode, SQLFunction
from pdql.dialects import Dialect, GenericDialect


@dataclass
class Join:
    table: Union[str, "SQLDataFrame"]
    join_type: str
    condition: SQLExpression
    alias: Optional[str] = None


class SQLDataFrame:
    """Immutable container representing a SQL query."""

    def __init__(
        self,
        source: Union[str, "SQLDataFrame"],
        select_cols: Optional[List[Union[str, SQLNode]]] = None,
        where_conditions: Optional[List[SQLExpression]] = None,
        joins: Optional[List[Join]] = None,
        group_by_cols: Optional[List[Union[str, SQLNode]]] = None,
        order_by: Optional[List[Tuple[SQLNode, bool]]] = None,
        limit_count: Optional[int] = None,
        alias_name: Optional[str] = None,
        dialect: Optional[Dialect] = None,
        ctes: Optional[Dict[str, "SQLDataFrame"]] = None,
    ):
        self.source = source
        self.select_cols = select_cols or ["*"]
        self.where_conditions = where_conditions or []
        self.joins = joins or []
        self.group_by_cols = group_by_cols or []
        self.order_by = order_by or []
        self.limit_count = limit_count
        self.alias_name = alias_name
        self.dialect = dialect
        self.ctes = ctes or {}

    @property
    def identifier(self) -> str:
        """Identifier used for table qualification."""
        if self.alias_name:
            return self.alias_name
        if isinstance(self.source, str):
            return self.source
        return self.source.identifier

    def is_simple(self) -> bool:
        """True if the dataframe is a simple table reference."""
        return (
            self.select_cols == ["*"]
            and not self.where_conditions
            and not self.joins
            and not self.group_by_cols
            and not self.order_by
            and self.limit_count is None
            and isinstance(self.source, str)
        )

    def alias(self, name: str) -> "SQLDataFrame":
        """Assign an alias for subquery usage."""
        return SQLDataFrame(
            source=self.source,
            select_cols=self.select_cols,
            where_conditions=self.where_conditions,
            joins=self.joins,
            group_by_cols=self.group_by_cols,
            order_by=self.order_by,
            limit_count=self.limit_count,
            alias_name=name,
            dialect=self.dialect,
            ctes=self.ctes,
        )

    def with_cte(self, name: str, dataframe: "SQLDataFrame") -> "SQLDataFrame":
        """Add a Common Table Expression to the query."""
        new_ctes = dict(self.ctes)
        new_ctes[name] = dataframe
        return SQLDataFrame(
            source=self.source,
            select_cols=self.select_cols,
            where_conditions=self.where_conditions,
            joins=self.joins,
            group_by_cols=self.group_by_cols,
            order_by=self.order_by,
            limit_count=self.limit_count,
            alias_name=self.alias_name,
            dialect=self.dialect,
            ctes=new_ctes,
        )

    def __getitem__(self, item: Any) -> Union[SQLColumn, "SQLDataFrame"]:
        if isinstance(item, str):
            owner = self.identifier if not self.joins else None
            return SQLColumn(item, owner=owner)

        if isinstance(item, list):
            return SQLDataFrame(
                source=self.source,
                select_cols=item,
                where_conditions=self.where_conditions,
                joins=self.joins,
                group_by_cols=self.group_by_cols,
                order_by=self.order_by,
                limit_count=self.limit_count,
                alias_name=self.alias_name,
                dialect=self.dialect,
                ctes=self.ctes,
            )

        if isinstance(item, SQLExpression):
            new_conditions = self.where_conditions + [item]
            return SQLDataFrame(
                source=self.source,
                select_cols=self.select_cols,
                where_conditions=new_conditions,
                joins=self.joins,
                group_by_cols=self.group_by_cols,
                order_by=self.order_by,
                limit_count=self.limit_count,
                alias_name=self.alias_name,
                dialect=self.dialect,
                ctes=self.ctes,
            )

        raise TypeError(f"Invalid argument type for __getitem__: {type(item)}")

    def merge(
        self,
        right: "SQLDataFrame",
        how: str = "inner",
        on: Optional[str] = None,
        left_on: Optional[str] = None,
        right_on: Optional[str] = None,
    ) -> "SQLDataFrame":
        """Merge with another SQLDataFrame."""
        if on:
            left_col = self[on]
            right_col = right[on]
            condition = left_col == right_col
        elif left_on and right_on:
            left_col = self[left_on]
            right_col = right[right_on]
            condition = left_col == right_col
        else:
            raise ValueError("Must specify 'on' or 'left_on' and 'right_on'")

        join_map = {
            "inner": "JOIN",
            "left": "LEFT JOIN",
            "right": "RIGHT JOIN",
            "outer": "FULL OUTER JOIN",
        }
        join_type = join_map.get(how, "JOIN")

        new_join = Join(
            table=right,
            join_type=join_type,
            condition=condition,
            alias=right.alias_name,
        )

        return SQLDataFrame(
            source=self.source,
            select_cols=self.select_cols,
            where_conditions=self.where_conditions,
            joins=self.joins + [new_join],
            group_by_cols=self.group_by_cols,
            order_by=self.order_by,
            limit_count=self.limit_count,
            alias_name=self.alias_name,
            dialect=self.dialect,
            ctes=self.ctes,
        )

    def groupby(
        self, by: Union[str, List[str], SQLNode, List[SQLNode]]
    ) -> "SQLDataFrame":
        if not isinstance(by, list):
            by = [by]

        return SQLDataFrame(
            source=self.source,
            select_cols=self.select_cols,
            where_conditions=self.where_conditions,
            joins=self.joins,
            group_by_cols=by,
            order_by=self.order_by,
            limit_count=self.limit_count,
            alias_name=self.alias_name,
            dialect=self.dialect,
            ctes=self.ctes,
        )

    def agg(self, func_map: Dict[str, str]) -> "SQLDataFrame":
        new_selects = []
        for grp in self.group_by_cols:
            if isinstance(grp, str):
                new_selects.append(self[grp])
            else:
                new_selects.append(grp)

        for col_name, func_name in func_map.items():
            col = self[col_name]
            alias = f"{col_name}_{func_name}"
            func_node = SQLFunction(func_name, col, alias=alias)
            new_selects.append(func_node)

        return SQLDataFrame(
            source=self.source,
            select_cols=new_selects,
            where_conditions=self.where_conditions,
            joins=self.joins,
            group_by_cols=self.group_by_cols,
            order_by=self.order_by,
            limit_count=self.limit_count,
            alias_name=self.alias_name,
            dialect=self.dialect,
            ctes=self.ctes,
        )

    def sort_values(
        self,
        by: Union[str, SQLNode, List[Union[str, SQLNode]]],
        ascending: Union[bool, List[bool]] = True,
    ) -> "SQLDataFrame":
        if not isinstance(by, list):
            by = [by]
        if not isinstance(ascending, list):
            ascending = [ascending] * len(by)

        new_order_by = list(self.order_by)
        for item, asc in zip(by, ascending):
            if isinstance(item, str):
                node = self[item]
            else:
                node = item
            new_order_by.append((node, asc))

        return SQLDataFrame(
            source=self.source,
            select_cols=self.select_cols,
            where_conditions=self.where_conditions,
            joins=self.joins,
            group_by_cols=self.group_by_cols,
            order_by=new_order_by,
            limit_count=self.limit_count,
            alias_name=self.alias_name,
            dialect=self.dialect,
            ctes=self.ctes,
        )

    def head(self, n: int = 5) -> "SQLDataFrame":
        return SQLDataFrame(
            source=self.source,
            select_cols=self.select_cols,
            where_conditions=self.where_conditions,
            joins=self.joins,
            group_by_cols=self.group_by_cols,
            order_by=self.order_by,
            limit_count=n,
            alias_name=self.alias_name,
            dialect=self.dialect,
            ctes=self.ctes,
        )

    def insert(self, data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> str:
        if not isinstance(self.source, str):
            raise ValueError("Can only insert into a table (string source)")

        if isinstance(data, dict):
            data = [data]

        if not data:
            raise ValueError("No data provided for insert")

        dialect = self.dialect or GenericDialect()
        columns = list(data[0].keys())
        quoted_table = dialect.quote_identifier(self.source)
        quoted_cols = ", ".join(dialect.quote_identifier(c) for c in columns)

        all_values = []
        for record in data:
            vals = ", ".join(dialect.format_value(record[c]) for c in columns)
            all_values.append(f"({vals})")

        values_str = ", ".join(all_values)
        return f"INSERT INTO {quoted_table} ({quoted_cols}) VALUES {values_str}"

    def delete(self) -> str:
        if not isinstance(self.source, str):
            raise ValueError("Can only delete from a table (string source)")

        dialect = self.dialect or GenericDialect()
        quoted_table = dialect.quote_identifier(self.source)
        sql = f"DELETE FROM {quoted_table}"

        if self.where_conditions:
            conditions = [cond.to_sql(dialect) for cond in self.where_conditions]
            where_clause = " AND ".join(conditions)
            sql += f" WHERE {where_clause}"

        return sql

    def to_sql(self, dialect: Optional[Dialect] = None) -> str:
        """Generate SQL query string."""
        if dialect is None:
            dialect = self.dialect or GenericDialect()

        if self.select_cols == ["*"]:
            select_clause = "*"
        else:
            quoted_cols = []
            for col in self.select_cols:
                if isinstance(col, SQLNode):
                    quoted_cols.append(col.to_sql(dialect))
                else:
                    quoted_cols.append(dialect.quote_identifier(col))
            select_clause = ", ".join(quoted_cols)

        if isinstance(self.source, str):
            from_clause = dialect.quote_identifier(self.source)
        elif self.source.is_simple() and not self.alias_name:
            from_clause = dialect.quote_identifier(self.source.source)  # type: ignore
        else:
            subquery_sql = self.source.to_sql(dialect)
            alias = dialect.quote_identifier(self.alias_name or self.identifier)
            from_clause = f"({subquery_sql}) AS {alias}"

        join_clauses = []
        for join in self.joins:
            if isinstance(join.table, str):
                table_sql = dialect.quote_identifier(join.table)
            elif join.table.is_simple() and not join.alias:
                table_sql = dialect.quote_identifier(join.table.source)  # type: ignore
            else:
                inner_sql = join.table.to_sql(dialect)
                alias = dialect.quote_identifier(join.alias or join.table.identifier)
                table_sql = f"({inner_sql}) AS {alias}"

            condition = join.condition.to_sql(dialect)
            join_clauses.append(f"{join.join_type} {table_sql} ON {condition}")

        full_from = f"{from_clause}"
        if join_clauses:
            full_from += " " + " ".join(join_clauses)

        sql = f"SELECT {select_clause} FROM {full_from}"

        if self.where_conditions:
            conditions = [cond.to_sql(dialect) for cond in self.where_conditions]
            where_clause = " AND ".join(conditions)
            sql += f" WHERE {where_clause}"

        if self.group_by_cols:
            group_items = []
            for g in self.group_by_cols:
                if isinstance(g, SQLNode):
                    group_items.append(g.to_sql(dialect))
                else:
                    owner = self.alias_name or (
                        self.source
                        if isinstance(self.source, str)
                        else self.source.identifier
                    )
                    quoted_owner = dialect.quote_identifier(owner)
                    quoted_col = dialect.quote_identifier(g)
                    group_items.append(f"{quoted_owner}.{quoted_col}")
            group_clause = ", ".join(group_items)
            sql += f" GROUP BY {group_clause}"

        if self.order_by:
            order_items = []
            for node, asc in self.order_by:
                direction = "ASC" if asc else "DESC"
                order_items.append(f"{node.to_sql(dialect)} {direction}")
            sql += f" ORDER BY {', '.join(order_items)}"

        if self.limit_count is not None:
            sql += f" LIMIT {self.limit_count}"

        if self.ctes:
            cte_parts = []
            for name, cte_df in self.ctes.items():
                cte_parts.append(
                    f"{dialect.quote_identifier(name)} AS ({cte_df.to_sql(dialect)})"
                )
            sql = f"WITH {', '.join(cte_parts)} {sql}"

        return sql