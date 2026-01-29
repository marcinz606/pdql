import pytest
from pdql.dataframe import SQLDataFrame


def test_insert_single():
    df = SQLDataFrame("users")
    sql = df.insert({"name": "Alice", "age": 30})
    assert sql == 'INSERT INTO "users" ("name", "age") VALUES (\'Alice\', 30)'


def test_insert_multiple():
    df = SQLDataFrame("users")
    data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
    sql = df.insert(data)
    expected = (
        'INSERT INTO "users" ("name", "age") VALUES (\'Alice\', 30), (\'Bob\', 25)'
    )
    assert sql == expected


def test_delete_with_filter():
    df = SQLDataFrame("users")
    sql = df[df["id"] == 1].delete()
    assert sql == 'DELETE FROM "users" WHERE ("users"."id" = 1)'


def test_delete_all():
    df = SQLDataFrame("users")
    sql = df.delete()
    assert sql == 'DELETE FROM "users"'
