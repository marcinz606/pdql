import pytest
from pdql.expressions import SQLColumn, SQLFunction
from pdql.dialects import GenericDialect


@pytest.fixture
def dialect():
    return GenericDialect()


def test_simple_function(dialect):
    col = SQLColumn("salary")
    func = SQLFunction("sum", col)
    assert func.to_sql(dialect) == 'SUM("salary")'


def test_function_alias(dialect):
    col = SQLColumn("salary")
    func = SQLFunction("avg", col, alias="avg_salary")
    assert func.to_sql(dialect) == 'AVG("salary") AS "avg_salary"'


def test_star_argument(dialect):
    func = SQLFunction("count", "*")
    assert func.to_sql(dialect) == "COUNT(*)"


def test_window_function_simple(dialect):
    col = SQLColumn("salary")
    func = SQLFunction("sum", col).over()
    assert func.to_sql(dialect) == 'SUM("salary") OVER ()'


def test_window_function_partition(dialect):
    col = SQLColumn("salary")
    dept = SQLColumn("department")

    func = SQLFunction("sum", col).over(partition_by=dept)
    assert func.to_sql(dialect) == 'SUM("salary") OVER (PARTITION BY "department")'


def test_window_function_order(dialect):
    col = SQLColumn("salary")
    date = SQLColumn("joined_date")
    func = SQLFunction("rank").over(order_by=date)
    assert func.to_sql(dialect) == 'RANK() OVER (ORDER BY "joined_date")'


def test_full_window_function(dialect):
    col = SQLColumn("salary")
    dept = SQLColumn("department")
    date = SQLColumn("joined_date")

    func = SQLFunction("sum", col, alias="running_total").over(
        partition_by=dept, order_by=date
    )

    expected = 'SUM("salary") OVER (PARTITION BY "department" ORDER BY "joined_date") AS "running_total"'
    assert func.to_sql(dialect) == expected
