import pytest
from pdql.expressions import SQLColumn
from pdql.dialects import GenericDialect, PostgresDialect, BigQueryDialect


@pytest.fixture
def dialect():
    return GenericDialect()


def test_column_representation(dialect):
    col = SQLColumn("my_col")
    assert col.to_sql(dialect) == '"my_col"'


def test_comparison_expression(dialect):
    col = SQLColumn("age")
    expr = col > 21
    assert expr.to_sql(dialect) == '("age" > 21)'


def test_arithmetic_expression(dialect):
    col = SQLColumn("salary")
    expr = (col * 12) + 500
    assert expr.to_sql(dialect) == '(("salary" * 12) + 500)'


def test_logical_expression(dialect):
    col1 = SQLColumn("is_adult")
    col2 = SQLColumn("has_permission")
    expr = (col1 == True) & (col2 == True)  # noqa: E712
    assert expr.to_sql(dialect) == '(("is_adult" = TRUE) AND ("has_permission" = TRUE))'


def test_string_literal(dialect):
    col = SQLColumn("name")
    expr = col == "Alice"
    assert expr.to_sql(dialect) == "(\"name\" = 'Alice')"


def test_postgres_dialect():
    pg_dialect = PostgresDialect()
    col = SQLColumn("user_id")
    assert col.to_sql(pg_dialect) == '"user_id"'


def test_bigquery_dialect():
    bq_dialect = BigQueryDialect()
    col = SQLColumn("project_id")
    assert col.to_sql(bq_dialect) == "`project_id`"


def test_nested_logic(dialect):
    col_a = SQLColumn("a")
    col_b = SQLColumn("b")
    expr = (col_a > 10) | ((col_b < 5) & (col_a != 20))
    assert expr.to_sql(dialect) == '(("a" > 10) OR (("b" < 5) AND ("a" != 20)))'
