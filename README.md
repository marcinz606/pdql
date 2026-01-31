# pdql

Lightweight Python library that allows you to write SQL queries using familiar Pandas syntax. It functions as a "lazy compiler," building a syntax tree from your operations and transpiling them into standard SQL strings without executing them or requiring a database connection.

## Installation

```bash
pip install pdql
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

### Advanced Functions & Method Chaining

Most standard SQL functions are available both as standalone functions and as methods on column objects for clean chaining.

```python
from pdql.dataframe import SQLDataFrame
from pdql import functions as f

df = SQLDataFrame("users")

# Method chaining on columns
query = df[df["email"].lower().starts_with("admin")]

# Complex transformations and types
query = query.groupby("status").agg({
    "salary": "mean",
    "id": "count"
})

print(query.to_sql())
# SELECT "status", AVG("salary") AS "salary_mean", COUNT("id") AS "id_count" 
# FROM "users" 
# WHERE (LOWER("users"."email") LIKE 'admin%') GROUP BY "status"
```

### Common Table Expressions (CTEs)

```python
# Define a subquery
sub = SQLDataFrame("raw_data")[["id", "val"]]
sub = sub[sub["val"] > 10]

# Use it as a source and define the CTE
df = SQLDataFrame("filtered").with_cte("filtered", sub)

print(df.to_sql())
# WITH "filtered" AS (SELECT "id", "val" FROM "raw_data" WHERE ("raw_data"."val" > 10)) 
# SELECT * FROM "filtered"
```

## Development

Use the `Makefile` for standard tasks:

- **Run Tests:** `make test`
- **Format Code:** `make format`
- **Linting:** `make lint`
- **Build Package:** `make build`

## License

[MIT](LICENSE.md)
