import pytest
from pdql.dataframe import SQLDataFrame
from pdql.expressions import SQLFunction


def test_sort_values_basic():
    df = SQLDataFrame("users")
    res = df.sort_values("age")
    assert res.to_sql() == 'SELECT * FROM "users" ORDER BY "users"."age" ASC'


def test_sort_values_descending():
    df = SQLDataFrame("users")
    res = df.sort_values("age", ascending=False)
    assert res.to_sql() == 'SELECT * FROM "users" ORDER BY "users"."age" DESC'


def test_sort_values_multiple():
    df = SQLDataFrame("users")
    res = df.sort_values(["last_name", "first_name"], ascending=[True, False])
    expected = 'SELECT * FROM "users" ORDER BY "users"."last_name" ASC, "users"."first_name" DESC'
    assert res.to_sql() == expected


def test_sort_by_function():
    df = SQLDataFrame("users")
    # order by RAND()
    res = df.sort_values(SQLFunction("rand"))
    assert res.to_sql() == 'SELECT * FROM "users" ORDER BY RAND() ASC'


def test_head():
    df = SQLDataFrame("users")
    res = df.head(10)
    assert res.to_sql() == 'SELECT * FROM "users" LIMIT 10'


def test_chained_sort_limit():
    df = SQLDataFrame("users")
    res = df[df["active"] == True].sort_values("created_at", ascending=False).head(5)

    expected = 'SELECT * FROM "users" WHERE ("users"."active" = TRUE) ORDER BY "users"."created_at" DESC LIMIT 5'
    assert res.to_sql() == expected
