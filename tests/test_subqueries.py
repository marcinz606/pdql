import pytest
from pdql.dataframe import SQLDataFrame


def test_basic_subquery():
    inner = SQLDataFrame("users")[["id", "name"]]
    inner = inner[inner["id"] > 100]

    outer = SQLDataFrame(inner).alias("filtered_users")

    expected = 'SELECT * FROM (SELECT "id", "name" FROM "users" WHERE ("users"."id" > 100)) AS "filtered_users"'
    assert outer.to_sql() == expected


def test_nested_subquery():
    df1 = SQLDataFrame("table1").alias("t1")[["col1"]]
    df2 = SQLDataFrame(df1).alias("t2")[["col1"]]
    df3 = SQLDataFrame(df2).alias("t3")

    sql = df3.to_sql()
    assert sql.count("SELECT") == 3
    assert '"t2"' in sql
    assert '"t3"' in sql


def test_join_with_subquery():
    users = SQLDataFrame("users")

    orders_agg = (
        SQLDataFrame("orders")
        .groupby("user_id")
        .agg({"id": "count"})
        .alias("order_counts")
    )

    res = users.merge(orders_agg, left_on="id", right_on="user_id")

    sql = res.to_sql()
    assert (
        'JOIN (SELECT "orders"."user_id", COUNT("orders"."id") AS "id_count" FROM "orders" GROUP BY "order_counts"."user_id") AS "order_counts"'
        in sql
    )
    assert 'ON ("users"."id" = "order_counts"."user_id")' in sql
