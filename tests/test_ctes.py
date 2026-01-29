import pytest
from pdql.dataframe import SQLDataFrame


def test_single_cte():
    sub = SQLDataFrame("raw_data")[["id", "val"]]
    sub = sub[sub["val"] > 10]
    
    df = SQLDataFrame("filtered").with_cte("filtered", sub)
    
    sql = df.to_sql()
    assert sql.startswith('WITH "filtered" AS (SELECT "id", "val" FROM "raw_data" WHERE ("raw_data"."val" > 10))')
    assert 'SELECT * FROM "filtered"' in sql


def test_multiple_ctes():
    cte1 = SQLDataFrame("t1").head(10)
    cte2 = SQLDataFrame("t2").head(20)
    
    df = SQLDataFrame("final").with_cte("c1", cte1).with_cte("c2", cte2)
    
    sql = df.to_sql()
    assert 'WITH "c1" AS (SELECT * FROM "t1" LIMIT 10), "c2" AS (SELECT * FROM "t2" LIMIT 20)' in sql
    assert 'SELECT * FROM "final"' in sql


def test_cte_propagation():
    sub = SQLDataFrame("raw").head(5)
    df = SQLDataFrame("cte_table").with_cte("cte_table", sub)
    
    filtered = df[df["id"] == 1]
    
    sql = filtered.to_sql()
    assert 'WITH "cte_table" AS' in sql
    assert 'WHERE ("cte_table"."id" = 1)' in sql
