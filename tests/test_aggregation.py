import pytest
from pdql.dataframe import SQLDataFrame
from pdql.dialects import GenericDialect


def test_groupby_simple():
    df = SQLDataFrame("sales")
    grouped = df.groupby("region")
    assert grouped.to_sql() == 'SELECT * FROM "sales" GROUP BY "sales"."region"'


def test_groupby_agg():
    df = SQLDataFrame("sales")
    res = df.groupby("region").agg({"amount": "sum"})

    expected = 'SELECT "sales"."region", SUM("sales"."amount") AS "amount_sum" FROM "sales" GROUP BY "sales"."region"'
    assert res.to_sql() == expected


def test_groupby_multiple_agg():
    df = SQLDataFrame("sales")
    res = df.groupby(["region", "year"]).agg({"amount": "sum", "id": "count"})

    expected = 'SELECT "sales"."region", "sales"."year", SUM("sales"."amount") AS "amount_sum", COUNT("sales"."id") AS "id_count" FROM "sales" GROUP BY "sales"."region", "sales"."year"'
    assert res.to_sql() == expected
