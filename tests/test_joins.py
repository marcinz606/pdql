import pytest
from pdql.dataframe import SQLDataFrame
from pdql.expressions import SQLColumn


def test_merge_simple_on():
    users = SQLDataFrame("users")
    orders = SQLDataFrame("orders")

    res = users.merge(orders, on="id")

    expected = 'SELECT * FROM "users" JOIN "orders" ON ("users"."id" = "orders"."id")'
    assert res.to_sql() == expected


def test_merge_left_on_right_on():
    users = SQLDataFrame("users")
    orders = SQLDataFrame("orders")

    res = users.merge(orders, left_on="id", right_on="user_id")

    expected = (
        'SELECT * FROM "users" JOIN "orders" ON ("users"."id" = "orders"."user_id")'
    )
    assert res.to_sql() == expected


def test_merge_left_join():
    users = SQLDataFrame("users")
    orders = SQLDataFrame("orders")

    res = users.merge(orders, how="left", on="id")

    expected = (
        'SELECT * FROM "users" LEFT JOIN "orders" ON ("users"."id" = "orders"."id")'
    )
    assert res.to_sql() == expected


def test_select_from_joined_tables():
    users = SQLDataFrame("users")
    orders = SQLDataFrame("orders")

    joined = users.merge(orders, on="id")

    res = joined[[users["name"], orders["amount"]]]

    expected = 'SELECT "users"."name", "orders"."amount" FROM "users" JOIN "orders" ON ("users"."id" = "orders"."id")'
    assert res.to_sql() == expected


def test_unqualified_selection_after_join():
    users = SQLDataFrame("users")
    orders = SQLDataFrame("orders")

    joined = users.merge(orders, on="id")

    res = joined[["status"]]

    expected = (
        'SELECT "status" FROM "users" JOIN "orders" ON ("users"."id" = "orders"."id")'
    )
    assert res.to_sql() == expected
