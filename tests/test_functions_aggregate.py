import pytest
from pdql.dataframe import SQLDataFrame
from pdql.functions import aggregate
from pdql.dialects import BigQueryDialect


def test_aggregate_functions():
    df = SQLDataFrame("t")
    
    assert aggregate.count().to_sql(BigQueryDialect()) == "COUNT(*)"
    assert aggregate.count(df["id"], is_distinct=True).to_sql(BigQueryDialect()) == "COUNT(DISTINCT `t`.`id`)"
    
    assert aggregate.sum(df["val"]).to_sql(BigQueryDialect()) == "SUM(`t`.`val`)"


def test_aggregate_in_dataframe():
    df = SQLDataFrame("orders")
    # Using agg method which uses SQLFunction under the hood
    res = df.groupby("user_id").agg({"amount": "sum"})
    sql = res.to_sql(BigQueryDialect())
    assert "SUM(`orders`.`amount`) AS `amount_sum`" in sql
