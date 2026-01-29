import pytest
from pdql.dataframe import SQLDataFrame
from pdql.dialects import GenericDialect, PostgresDialect, BigQueryDialect


@pytest.fixture
def df():
    return SQLDataFrame("users")


def test_basic_select_all(df):
    assert df.to_sql() == 'SELECT * FROM "users"'


def test_select_columns(df):
    new_df = df[["name", "age"]]
    assert new_df.to_sql() == 'SELECT "name", "age" FROM "users"'
    assert df.to_sql() == 'SELECT * FROM "users"'


def test_column_access_and_filter(df):
    new_df = df[df["age"] > 21]
    assert new_df.to_sql() == 'SELECT * FROM "users" WHERE ("users"."age" > 21)'


def test_multiple_filters(df):
    new_df = df[df["age"] > 21]
    new_df = new_df[new_df["status"] == "active"]

    expected = 'SELECT * FROM "users" WHERE ("users"."age" > 21) AND ("users"."status" = \'active\')'
    assert new_df.to_sql() == expected


def test_select_and_filter(df):
    new_df = df[["name", "email"]]
    new_df = new_df[df["id"] != 0]

    expected = 'SELECT "name", "email" FROM "users" WHERE ("users"."id" != 0)'
    assert new_df.to_sql() == expected


def test_dialect_support():
    df = SQLDataFrame("my_table")
    pg_dialect = PostgresDialect()
    assert df.to_sql(pg_dialect) == 'SELECT * FROM "my_table"'


def test_persistent_dialect():
    bq = BigQueryDialect()
    df = SQLDataFrame("my_table", dialect=bq)

    assert df.to_sql() == "SELECT * FROM `my_table`"

    filtered = df[df["id"] > 1]
    assert filtered.to_sql() == "SELECT * FROM `my_table` WHERE (`my_table`.`id` > 1)"
