# pdql

Lightweight Python library that allows you to write SQL queries using familiar Pandas syntax. It functions as a "lazy compiler," building a syntax tree from your operations and transpiling them into standard SQL strings without executing them or requiring a database connection.

## Installation

Clone the repository and set up the environment using the provided Makefile:

```bash
git clone <repo-url>
cd pdql
make setup
```

## Usage

### Persistent Dialect & Filtering

```python
from pdql.dataframe import SQLDataFrame
from pdql.dialects import BigQueryDialect

# Initialize with a specific dialect
df = SQLDataFrame("my_table", dialect=BigQueryDialect())

# Filters use dialect-specific quoting (backticks for BigQuery)
query = df[df["age"] > 21]

print(query.to_sql())
# SELECT * FROM `my_table` WHERE (`my_table`.`age` > 21)
```

### Common Table Expressions (CTEs)

```python
from pdql.dataframe import SQLDataFrame

# Define a subquery
sub = SQLDataFrame("raw_data")[["id", "val"]]
sub = sub[sub["val"] > 10]

# Use it as a source and define the CTE
df = SQLDataFrame("filtered").with_cte("filtered", sub)

print(df.to_sql())
# WITH "filtered" AS (SELECT "id", "val" FROM "raw_data" WHERE ("raw_data"."val" > 10)) SELECT * FROM "filtered"
```

### Subqueries & Aliasing

```python
inner = SQLDataFrame("orders").groupby("user_id").agg({"amount": "sum"}).alias("totals")
outer = SQLDataFrame(inner)
query = outer[outer["amount_sum"] > 1000]

print(query.to_sql())
# SELECT * FROM (SELECT "user_id", SUM("amount") AS "amount_sum" FROM "orders" GROUP BY "user_id") AS "totals" WHERE ("totals"."amount_sum" > 1000)
```

### Ordering & Limits

```python
from pdql.expressions import SQLFunction

# Order by columns or expressions/functions
query = df.sort_values(["created_at", SQLFunction("rand")], ascending=[False, True]).head(10)

print(query.to_sql())
# SELECT * FROM "my_table" ORDER BY "my_table"."created_at" DESC, RAND() ASC LIMIT 10
```

### DML Operations

```python
df = SQLDataFrame("users")

# Generate INSERT
insert_sql = df.insert({"name": "Alice", "status": "active"})

# Generate DELETE based on current filters
delete_sql = df[df["status"] == "inactive"].delete()
```

## Development

Use the `Makefile` for standard tasks:

- **Run Tests:** `make test`
- **Format Code:** `make format`
- **Linting:** `make lint`
- **Build Package:** `make build`

## License

[MIT](LICENSE.md)
