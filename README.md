# pdql

**pdql** is a lightweight, type-safe Python library that allows you to write SQL queries using familiar Pandas syntax. It functions as a "lazy compiler," building a syntax tree from your operations and transpiling them into standard SQL strings without executing them or requiring a database connection.

## Key Features

- **Pandas-like Syntax:** Leverage your existing knowledge of Pandas methods like `[]`, `merge`, `groupby`, and `agg`.
- **Comprehensive Function Library:** Over 100+ BigQuery-compatible functions (`math`, `string`, `datetime`, `json`, `geography`, etc.).
- **Subqueries & Modularity:** Use one `SQLDataFrame` as a source for another, automatically generating nested subqueries with aliasing.
- **Common Table Expressions (CTEs):** Define reusable subqueries using `with_cte()`.
- **Dialect Support:** Persistent dialect settings (ANSI, PostgreSQL, BigQuery) that propagate through all transformations.
- **Immutable:** Adheres to functional programming principles—every transformation returns a new instance.

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

### Date & Geography Examples

```python
from pdql import functions as f

# Extracting parts from dates
df = SQLDataFrame("events")
df["hour"] = f.extract("HOUR", df["created_at"])

# Geographical calculations
p1 = f.st_geogpoint(-122.33, 47.60) # Seattle
p2 = f.st_geogpoint(-118.24, 34.05) # LA
df["dist_to_hq"] = f.st_distance(df["location"], p1)

print(df.to_sql())
# SELECT *, EXTRACT(HOUR FROM "events"."created_at") AS "hour", 
# ST_DISTANCE("events"."location", ST_GEOGPOINT(-122.33, 47.60)) AS "dist_to_hq" 
# FROM "events"
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

[MIT](LICENSE)