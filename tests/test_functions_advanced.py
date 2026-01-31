import pytest
from pdql.dataframe import SQLDataFrame
from pdql.functions import (
    json_value, array_length, sha256, host, st_distance
)
from pdql.dialects import BigQueryDialect


def test_json_functions():
    df = SQLDataFrame("t")
    assert json_value(df["info"], "$.name").to_sql(BigQueryDialect()) == "JSON_VALUE(`t`.`info`, '$.name')"


def test_array_functions():
    df = SQLDataFrame("t")
    assert array_length(df["items"]).to_sql(BigQueryDialect()) == "ARRAY_LENGTH(`t`.`items`)"


def test_crypto_functions():
    df = SQLDataFrame("t")
    assert sha256(df["pw"]).to_sql(BigQueryDialect()) == "SHA256(`t`.`pw`)"


def test_net_functions():
    df = SQLDataFrame("t")
    assert host(df["url"]).to_sql(BigQueryDialect()) == "NET.HOST(`t`.`url`)"


def test_geography_functions():
    df = SQLDataFrame("t")
    col = st_distance(df["p1"], df["p2"])
    assert col.to_sql(BigQueryDialect()) == "ST_DISTANCE(`t`.`p1`, `t`.`p2`)"
