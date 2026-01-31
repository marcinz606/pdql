import pytest
from pdql.dataframe import SQLDataFrame
from pdql.functions import datetime
from pdql.dialects import BigQueryDialect


def test_datetime_functions():
    df = SQLDataFrame("t")
    
    assert datetime.current_date().to_sql(BigQueryDialect()) == "CURRENT_DATE()"
    
    # Test extract
    col_hour = datetime.extract("HOUR", df["ts"])
    assert col_hour.to_sql(BigQueryDialect()) == "EXTRACT(HOUR FROM `t`.`ts`)"
    
    # Test date_add
    col_add = datetime.date_add(df["d"], "INTERVAL 1 DAY")
    assert col_add.to_sql(BigQueryDialect()) == "DATE_ADD(`t`.`d`, 'INTERVAL 1 DAY')"
