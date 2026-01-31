import pytest
from pdql.dataframe import SQLDataFrame
from pdql.functions import math
from pdql.dialects import BigQueryDialect, PostgresDialect


def test_math_functions_basic():
    df = SQLDataFrame("t")
    
    col_abs = math.abs(df["x"])
    assert col_abs.to_sql(BigQueryDialect()) == 'ABS(`t`.`x`)'
    
    col_round = math.round(df["x"], 2)
    assert col_round.to_sql(BigQueryDialect()) == 'ROUND(`t`.`x`, 2)'


def test_math_functions_on_column():
    df = SQLDataFrame("t")
    
    # Test column methods
    assert df["x"].abs().to_sql(BigQueryDialect()) == 'ABS(`t`.`x`)'
    assert df["x"].ceil().to_sql(PostgresDialect()) == 'CEIL("t"."x")'
    assert df["x"].round(1).to_sql(BigQueryDialect()) == 'ROUND(`t`.`x`, 1)'


def test_cast_function():
    df = SQLDataFrame("t")
    col_cast = df["x"].cast("FLOAT64")
    assert col_cast.to_sql(BigQueryDialect()) == 'CAST(`t`.`x` AS FLOAT64)'