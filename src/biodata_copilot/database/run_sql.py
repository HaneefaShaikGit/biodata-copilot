import sys
from pathlib import Path

import duckdb


query_file = sys.argv[1]

sql = Path(query_file).read_text()

connection = duckdb.connect("data/biodata.duckdb")

result = connection.execute(sql).fetchdf()

print(result.to_string(index=False))

connection.close()