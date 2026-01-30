import pytest
from pdql.dataframe import SQLDataFrame
from pdql.functions import string
from pdql.dialects import BigQueryDialect, PostgresDialect


def test_string_functions_basic():
    df = SQLDataFrame("t")
    
    col_upper = string.upper(df["name"])
    assert col_upper.to_sql(BigQueryDialect()) == 'UPPER(`t`.`name`)'
    
    col_concat = string.concat(df["a"], "-", df["b"])
    assert col_concat.to_sql(BigQueryDialect()) == "CONCAT(`t`.`a`, '-', `t`.`b`)"


def test_string_functions_on_column():
    df = SQLDataFrame("t")
    
    assert df["name"].upper().to_sql(PostgresDialect()) == 'UPPER("t"."name")'
    assert df["name"].lower().to_sql(BigQueryDialect()) == 'LOWER(`t`.`name`)'


def test_regexp_replace():
    df = SQLDataFrame("t")
    col = string.regexp_replace(df["txt"], r"\d+", "NUM")
    assert col.to_sql(BigQueryDialect()) == r"REGEXP_REPLACE(`t`.`txt`, '\d+', 'NUM')"
